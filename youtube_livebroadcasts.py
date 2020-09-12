import time

class API:
    def __init__(self, youtube):
        self.api = youtube.liveBroadcasts()

    def get_info(self, part="snippet,contentDetails,status", livebroadcat_id=None):
        if livebroadcat_id:
            request = self.api.list(part=part, broadcastType="all", id=livebroadcat_id)
        else:
            request = self.api.list(part=part, broadcastType="all", mine=True)

        response = request.execute()
        return response

    def get_status(self, livebroadcat_id):
        response = self.get_info(part="status", livebroadcat_id=livebroadcat_id)
        return response["items"][0]["status"]["lifeCycleStatus"]

    def wait_for_changing_status(self, livebroadcat_id, target_status, ptime_sec=5):
        while True :
            status = self.get_status(livebroadcat_id)
            print(f"livebroadcast_status: {status} (expected {target_status})")
            if status == target_status:
                break
            time.sleep(ptime_sec)

    def delete(self, livebroadcat_id):
        request = self.api.delete(id=livebroadcat_id)
        response = request.execute()
        return response       

    def delete_all(self):
        request = self.api.list(part="snippet,status", broadcastType="all", mine=True)
        response = request.execute()
        for item in response['items']:
            request = self.api.delete(id=item["id"])
            response = request.execute()
        return response

    def create(self, title, scheduled_start_time):
        request = self.api.insert(
            part="snippet,contentDetails,status",
            body={
                "contentDetails": {
                    "enableClosedCaptions": True,
                    "enableContentEncryption": True,
                    "enableDvr": False,
                    "enableEmbed": False, # Falseじゃないと400 error
                    "recordFromStart": True, # Trueじゃないと403 error
                    "startWithSlate": False,
                    "enableAutoStart": False,
                    "enableAutoStop": False,
                    "monitorStream": {
                        "enableMonitorStream":True
                    }
                },
                "snippet": {
                    "title": title,
                    "description": "this livebroadcast is {}".format(title),
                    "scheduledStartTime": scheduled_start_time # "2020-09-10T19:00:00Z"
                },
                "status": {
                    "privacyStatus": "private"
                }
            }
        )
        response = request.execute()
        return response

    def bind(self, livebroadcasts_id, livestream_id):
        request = self.api.bind(
            part="snippet",
            id=livebroadcasts_id,
            streamId=livestream_id
        )
        response = request.execute()
        return response       

    def transition_status(self, livebroadcasts_id, status):
        request = self.api.transition(
            part="snippet,status",
            id=livebroadcasts_id,
            broadcastStatus=status,
        )
        response = request.execute()
        return response