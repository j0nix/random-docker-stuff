# Docker Swarm
**Setup a Docker swarm demo env with GlusterFS volume replication for persistent storage**

## Preparations
**1. Setup 3 nodes swarm cluster with following roles:**
- 1 manager
- 2 workers

**2. create a wildcard record pointing to a loadbalancer**
 - *Configure HTTPS to terminate TLS on the LB, also add a certificate valid for your wildcard domain*
 - *Configure LB to sent (http) traffic to port 8081 on the manager node*

**3. Setup GlusterFS**
 - *3 CentOS7 NODEs, EACH NODE HAVE BEEN ADDED A 5G DISK IN VMWARE BEFORE PROCEED WITH BELOW*

```
[ON ALL NODES]
yum -y install centos-release-gluster9 && yum -y install glusterfs glusterfs-cli glusterfs-libs glusterfs-server
systemctl enable glusterd.service && systemctl start glusterd.service
pvcreate /dev/sd<?> && vgcreate glusterfs /dev/sd<?>
lvcreate -L 5G -n brick1 glusterfs && mkfs.xfs /dev/mapper/glusterfs-brick1 && mkdir -p /opt/glusterfs/brick1
echo "/dev/mapper/glusterfs-brick1 /opt/glusterfs/brick1 xfs defaults 0 0" >> /etc/fstab
mount -a
mkdir /opt/glusterfs/brick1/volume1

[ON THAT SWARM MANAGER NODE]
gluster peer probe server2
gluster peer probe server3
gluster volume create my-volume-1 replica 3 transport tcp <server-1-ip>:/opt/glusterfs/brick1/volume1 <server-2-ip>:/opt/glusterfs/brick1/volume1 <server-3-ip>:/opt/glusterfs/brick1/volume1
gluster volume start my-volume-1
gluster volume set my-volume-1 auth.allow server-1,server-2,server-3
 
[ON ALL NODES]
mkdir -p /data/glusterfs/j0nixService1
echo "localhost:/my-volume-1 /data/glusterfs/j0nixService1  glusterfs  defaults,_netdev,backupvolfile-server=localhost  0 0" >> /etc/fstab
mount -a
```
## Create the ingress controller
**1. Create a ingress network**
- `docker network create -d overlay --attachable traefik-public`

**2. Clone this repo to manager node**
 - *... and enter the cloned repository*

**3. Prep that traefik settings file avaliable
- mkdir -p /opt/docker/traefik && cp ingress-controller/traefik.yml /opt/docker/traefik

**4. Deploy that ingress controller**
*Note that the ingress controller will only be deployed on the manager* 
 - ` docker stack deploy -c ingress-controller/traefik_deployment.yml traefik `

## Prep a html file for that demo
***[ON THAT SWARM MANAGER NODE]***

`echo "<html><head><title>DEMO</title></head><body><h2>docker stack deploy -c j0nix_deployments.yml demo</h2><pre>" > /data/glusterfs/j0nixService1/index.html && cat demo-services/j0nix_deployments.yml >> /data/glusterfs/j0nixService1/index.html && echo "</pre></body></html>" >> /data/glusterfs/j0nixService1/index.html`

## Deploy demo services
***[ON THAT SWARM MANAGER NODE]***

**- Adjust label 'traefik.http.routers.j0nixService1.rule' in demo-services/j0nix_deployments.yml to fit your environment**
 - `docker stack deploy -c demo-services/j0nix_deployments.yml demo `

**- Adjust label 'traefik.http.routers.j0nixService1.rule' in demo-services/service2service/service2service_deploy.yml to fit your environment**
 - `docker stack deploy -c demo-services/service2service/service2service_deploy.yml demo2`


## What do we have here...?
**demo-services/j0nix_deployments.yml** - deploys services **j0nixService1** and **j0nixService2**. 

- j0nixService 1 mounts that index.html file we have in out glusterfs replication. 
  update it on the manager node and see the changes gets replicated to service running on a worker node.

- j0nixService2 demos that you loadbalance between containers on your requests to them

**demo-services/service2service/service2service_deploy.yml** - Deploys a service calling **j0nixService3**. 

 - Demo a service calling another service within the swarm cluster.



