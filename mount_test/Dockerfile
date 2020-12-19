# j0nix-2020
FROM alpine:latest
# Install cifs & sudo
RUN apk add cifs-utils sudo
# Allow nobody to run sudo mount -a without password prompt
RUN echo "nobody ALL=(ALL) NOPASSWD: /bin/mount -a" > /etc/sudoers.d/nobody
# copy fstab data & user credentials to 
COPY fstab_shares /tmp/
COPY mount_credentials /etc/
RUN chown root:root /etc/mount_credentials && chmod 0600 /etc/mount_credentials
# add your shares to fstab
RUN cat /tmp/fstab_shares >> /etc/fstab
# make sure we have those local directorys defined in fstab
RUN for dir in $(cat /tmp/fstab_shares|cut -d\  -f2); do mkdir -p $dir;done
# Script that mounts all and do whatever ... 
COPY start.sh .
ENTRYPOINT ./start.sh
