gst-launch-1.0 filesrc location=stop.mp3 \
                        	! mpegaudioparse \
                        	! mpg123audiodec \
                        	! audioconvert \
                        	! audioresample \
                        	! audio/x-raw, rate=16000, channels=1, format=S16LE \
                        	! audiomixer blocksize=320 \
                        	! udpsink host=127.0.0.1 port=10000
