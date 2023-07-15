import os
import streamlit as st
from pytube import YouTube


def main():
    st.title("YouTube Video Downloader")

    # Input box for YouTube URL
    video_url = st.text_input("Enter the YouTube URL")

    if st.button("Download"):
        # Check if the URL is valid
        if not video_url:
            st.warning("Please enter a YouTube URL.")
            return

        try:
            # Create a YouTube object
            yt = YouTube(video_url)

            # Filter streams to high quality options (720p or 1080p)
            streams = yt.streams.filter(
                progressive=True, file_extension="mp4", resolution=lambda res: res in ["720p", "1080p"])

            # Get the available quality options
            quality_options = [
                f"{stream.resolution} ({stream.fps}fps)" for stream in streams]

            if not quality_options:
                st.warning(
                    "No high-quality video streams available (720p or 1080p).")
                return

            # Display quality options
            selected_quality = st.selectbox("Select Quality", quality_options)

            # Find the selected stream based on the quality
            stream = None
            for s in streams:
                if f"{s.resolution} ({s.fps}fps)" == selected_quality:
                    stream = s
                    break

            # Get the file size
            file_size = round(stream.filesize / (1024 * 1024), 2)
            st.info(f"File Size: {file_size} MB")

            # Download the stream
            st.info("Downloading...")
            file_path = stream.download(filename="temp")
            st.success("Download completed!")

            # Rename the file to remove the "temp" suffix
            renamed_file_path = os.path.join(
                os.getcwd(), f"{stream.default_filename}")
            os.rename(file_path, renamed_file_path)

            st.info(f"File saved at: {renamed_file_path}")

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

    # Contact section
    st.markdown("---")
    st.header("Contact Information")
    st.markdown("Name: Pushpankar Singh")
    st.markdown(
        "LinkedIn: [Pushpankar Singh](https://www.linkedin.com/in/pushpankarsingh/)")
    st.markdown("GitHub: [kpushpankar2](https://github.com/kpushpankar2)")


if __name__ == "__main__":
    main()
