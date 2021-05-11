# opencv gstreamer 파이프라인 해서 보낼 때 CLI 로 받는 코드
gst-launch-1.0 -v udpsrc port=1234 caps = "application/x-rtp, media=(string)video, clock-rate=(int)90000, encoding-name=(string)H264, payload=(int)96" ! rtpjitterbuffer ! rtph264depay ! decodebin ! videoconvert ! autovideosink
