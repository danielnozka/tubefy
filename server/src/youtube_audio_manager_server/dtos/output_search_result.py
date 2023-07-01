class OutputSearchResult:

    video_id: str
    video_title: str
    video_thumbnail_url: str

    def __init__(self,
                 video_id: str,
                 video_title: str,
                 video_thumbnail_url: str):

        self.video_id = video_id
        self.video_title = video_title
        self.video_thumbnail_url = video_thumbnail_url
