import time

class API:
    def __init__(self, youtube):
        self.api = youtube.liveStreams()

    def get_info(self, part="snippet,cdn,contentDetails,status", livestream_id=None):
        if livestream_id:
            request = self.api.list(part=part, id=livestream_id)
        else:
            request = self.api.list(part=part, mine=True)

        response = request.execute()
        return response

    def get_status(self, livestream_id):
        response = self.get_info(part="status", livestream_id=livestream_id)
        return response["items"][0]["status"]["streamStatus"]

    def wait_for_changing_status(self, livestream_id, target_status, ptime_sec=5):
        while True :
            status = self.get_status(livestream_id)
            print(f"livestream_status: {status} (expected {target_status})")
            if status == target_status:
                break
            time.sleep(ptime_sec)

    def delete(self, livestream_id):
        request = self.api.delete(id=livestream_id)
        response = request.execute()
        return response

    def delete_all(self):
        request = self.api.list(part="snippet,cdn,contentDetails,status", mine=True)
        response = request.execute()
        for item in response['items']:
            request = self.api.delete(id=item["id"])
            response = request.execute()
        return response

    def create(self, title, ingestion_type="rtmp", frame_rate="variable", resolution="variable"):
        request = self.api.insert(
            part="snippet,cdn,contentDetails,status",
            body={
                "cdn": {
                    "ingestionType": ingestion_type,
                    "frameRate": frame_rate,
                    "resolution": resolution
                },
                "contentDetails": {
                    "isReusable": True
                },
                "snippet": {
                    "title": title,
                    "description": "this livestream is {}".format(title)
                }
            }
        )

        response = request.execute()
        return response