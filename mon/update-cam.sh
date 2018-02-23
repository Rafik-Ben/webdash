#!/bin/bash
WWWPATH=/media/1TB/www
HOST=77.222.56.205
USER=ftpuser
PASS=ftppass
FILE=/tmp/camera.jpg

cd $WWWPATH
today=`date +%Y%m%d`
p="/media/1TB/ftp/camera/$today"
if [ -d "$p" ]; then
  f="$p/`ls -1 /media/1TB/ftp/camera/$today|tail -n1`"
  if [ -s "$f" ]; then
    #logger -t "$0" "Upload camera file: $f"
    FCAM=/tmp/camera.jpg
    cp $f $FCAM ## convert instead of cp
    #convert "$f" -gravity SouthEast -pointsize 22  -fill white -annotate +10+10 $(date +%F_%T) "$FCAM"
    ftp -in $HOST << EOF
user $USER $PASS
put $FILE camera.jpg
bye
EOF
    #logger -t "$0" "Upload: $?"
  else
    logger -t "$0" "File is empty: $f"
  fi
else
  logger -t "$0" "No such directory: $p"
  logger -t "$0" "Will not upload file $today"
fi

