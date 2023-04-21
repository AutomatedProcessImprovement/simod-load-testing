# simod-load-testing

![build](https://github.com/AutomatedProcessImprovement/simod-load-testing/actions/workflows/build.yaml/badge.svg)
![version](https://img.shields.io/github/v/tag/AutomatedProcessImprovement/simod-load-testing)

## Scalability Experiment

Mongo query to count finished requests:

```json
db.requests.count({ status: {$eq: 'succeeded' } })
```

Mongo query to find the earliest timestamp:

```json
db.requests.find({ finished_timestamp: { $exists: true, $ne: null } }).sort({ created_timestamp: 1 }).limit(1)
```

Mongo query to find the latest timestamp:

```json
db.requests.find({ finished_timestamp: { $exists: true, $ne: null } }).sort({ finished_timestamp: -1 }).limit(1)
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
mongoexport --db=simod --collection=requests --type=json --out=out.json -u root -p example --authenticationDatabase=admin
```

Copy the file from a pod to the local machine:

```bash
kubectl cp <pod-name>:out.json ./out.json
```
