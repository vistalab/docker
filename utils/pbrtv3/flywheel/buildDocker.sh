docker build -t vistalab/pbrt-v3-spectral:flywheel .
docker push vistalab/pbrt-v3-spectral:flywheel

docker tag vistalab/pbrt-v3-spectral:flywheel gcr.io/primal-surfer-140120/pbrt-v3-spectral-flywheel

gcloud docker -- push gcr.io/primal-surfer-140120/pbrt-v3-spectral-flywheel