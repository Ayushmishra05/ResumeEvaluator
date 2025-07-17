from resume_process.processapi import app as process_app 
from resume_uploader.resume_uploader import app as uploader_app
from multiprocessing import Process


def run_process():
    process_app.run(port=8000, debug=True, use_reloader=False)

def run_uploader():
    uploader_app.run(port=5000, debug=True, use_reloader=False)

if __name__ == '__main__':
    p1 = Process(target=run_process)
    p2 = Process(target=run_uploader)
    p1.start()
    p2.start()
    p1.join()
    p2.join()
