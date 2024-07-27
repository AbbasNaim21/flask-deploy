```sh 
docker build -t french-translator/api-server -f Dockerfile .
```
```sh 
docker run -p 8000:8000 french-translator/api-server
```

```sh
ngrok http 8000
```

```sh 
docker run -it --rm -e NGROK_AUTHTOKEN=2jk31ESrwm7P6luVzGjBc6ooJnU_6StQYn7oHFSoEQFYUYurJ ngrok/ngrok:latest http 172.17.0.2:8000
```