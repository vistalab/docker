docker build -t vistalab/pbrt-v3-spectral:gcloud .
docker push vistalab/pbrt-v3-spectral:gcloud

docker tag vistalab/pbrt-v3-spectral:gcloud gcr.io/primal-surfer-140120/pbrt-v3-spectral-gcloud

gcloud docker -- push gcr.io/primal-surfer-140120/pbrt-v3-spectral-gcloud