import os
import subprocess
import time
from datetime import datetime

#Directories/Folders involved
INPUT_DIR = "./input"
OUTPUT_DIR = "./output"
LOG_FILE = "./logs/pipeline.log"

#Log Entry Format and Log File Updation
def log_message(level, message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] [{level}] {message}\n"
    print(log_entry.strip())
    with open(LOG_FILE, "a") as f:
        f.write(log_entry)

#CPU Load / Performance Status
def get_cpu_status():
    try:
        with open("/proc/cpuinfo" , "r") as f:
            for line in f:
                if line.startswith("cpu MHz"):
                    freq_mhz = float(line.split(":")[1].strip())
                    freq_ghz = round(freq_mhz / 1000 , 2)
                    return f"{freq_ghz} GHz"
    except Exception as e:
        return f"Metrics Unavailable ({type(e).__name__})"
    
#Process the files in input folder
def process_media(file_name):
    input_path: str = os.path.join(INPUT_DIR , file_name)
    unique_prefix = datetime.now().strftime("LOT-%Y-%m-%d-%H%M%S")
    base_name, _ = os.path.splitext(file_name)
    output_file_name = f"{unique_prefix}_{base_name}.mp4"
    output_path: str = os.path.join(OUTPUT_DIR, output_file_name)

    log_message("INFO" , f"Starting processing for: {file_name} | CPU Speed: {get_cpu_status()}")

#Converting files to H.264 video with AAC audio
    ffmpeg_cmd = [
        "ffmpeg" , "-y",
        "-i", input_path,
        "-c:v", "libx264",
        "-preset", "fast",
        "-c:a", "aac",
        "-b:a", "192k",
        output_path
]

#Running FFmpeg in background to have clean logs
    try:
        result = subprocess.run(ffmpeg_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        log_message("SUCCESS" , f"Successfully transcoded to {output_file_name} | CPU Speed: {get_cpu_status()}")

        #Cleaning up input directory after success
        os.remove(input_path)
        log_message("INFO", f"Cleaned up source file from ingest pool: {file_name}")

    except subprocess.CalledProcessError as e:
        log_message("Error", f"FFmpeg failed processing {file_name}. Reason: {e.stderr}")

#Running the script as a background service(daemon)
def monitor_ingest_pool():
    log_message("System", f"Media Ingestion Engine started. Monitoring {INPUT_DIR} directory..")

    try:
        while True:
            files = [f for f in os.listdir(INPUT_DIR) if os.path.isfile(os.path.join(INPUT_DIR , f))]

            for file in files:
                if file.startswith('.'):
                    continue
                process_media(file)
                    
            time.sleep(2)
    except KeyboardInterrupt:
        log_message("System" , "Ingestion pipeline shut down cleanly by user")

if __name__ == "__main__":
    monitor_ingest_pool()
