# simod-load-testing

![build](https://github.com/AutomatedProcessImprovement/simod-load-testing/actions/workflows/build.yaml/badge.svg)
![version](https://img.shields.io/github/v/tag/AutomatedProcessImprovement/simod-load-testing)

This repository contains the load testing scripts for [simod-on-containers](https://github.com/AutomatedProcessImprovement/simod-on-containers), a solution for scalable business process discovery using Kubernetes as the container orchestration platform.

This repository provides a container image for the testing. The testing itself is executed using a Kubernetes manifest file such as [locust-scalability-travel.yaml](https://github.com/AutomatedProcessImprovement/simod-on-containers/blob/main/deploy/kind/locust-scalability-travel.yaml) or [locust-scalability-payments.yaml](https://github.com/AutomatedProcessImprovement/simod-on-containers/blob/main/deploy/kind/locust-scalability-payments.yaml).

Below you can find sample MongoDB queries to retrieve data for the scalability experiment.

## Scalability Experiment

Mongo query to count finished requests:

```json
db.requests.count({ status: {$eq: 'succeeded' } })
```

Mongo query to calculate duration of the experiment in milliseconds:

```json
db.requests.aggregate([
    {
        $match: {
            finished_timestamp: { $exists: true, $ne: null }
        }
    },
    {
        $project: {
            _id: 1,
            start: {
                $min: ["$created_timestamp"]
            },
            end: {
                $max: ["$finished_timestamp"]
            }
        }
    },
    {
        $group: {
            _id: null,
            start: {
                $min: "$start"
            },
            end: {
                $max: "$end"
            }
        },
    },
    {
        $project: {
            _id: 0,
            duration: {
                $subtract: ["$end", "$start"]
            }
        }
    }
])
```

Mongo query to calculate the duration of each request:

```json
db.requests.aggregate([
  {
    $match: {
      finished_timestamp: { $exists: true, $ne: null }
    }
  },
  {
    $project: {
      _id: 1,
      duration: {
        $subtract: ["$finished_timestamp", "$created_timestamp"]
      }
    }
  }
])
```

Export the database to a file:

```bash
mongoexport --db=simod --collection=requests --type=json --out=requests.json -u root -p example --authenticationDatabase=admin
```

Copy the file from a pod to the local machine:

```bash
kubectl cp <pod-name>:requests.json ./requests.json
```
