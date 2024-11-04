import srt
from datetime import timedelta

class SRTCompose:
    def __init__(self) -> None:
        self.subs = []
        self.idx = 1

    def append(self, sub: srt.Subtitle | dict):
        if isinstance(sub, dict):
            sub = srt.Subtitle(
                index=self.idx,
                start=timedelta(seconds=sub["start"]),
                end=timedelta(seconds=sub["end"]),
                content=sub["text"],
            )
        else:
            sub.index = self.idx

        self.idx += 1
        self.subs.append(sub)

    def append_bulk(self, subs):
        for sub in subs:
            self.append(sub)

    def save(self, path):
        file_content = srt.compose(self.subs)
        with open(path, "w") as f:
            f.write(file_content)
        print("file saved")

srt_compose = SRTCompose()