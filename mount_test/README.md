# README

## docker build 
`$ docker build -t mount_test .`

## docker run example:
`$ docker run --rm -it --user nobody --cap-add SYS_ADMIN --cap-add DAC_READ_SEARCH mount_test`
