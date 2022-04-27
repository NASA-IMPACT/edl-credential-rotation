# edl-credential-rotation
AWS stack to update another Lambda's environment settings with new Cumulus Distribution API [temporary S3 credentials](https://nasa.github.io/cumulus-distribution-api/#temporary-s3-credentials) every 30 minutes.


## Requirements
- Python>=3.8
- Docker
- tox
- aws-cli
- An IAM role with sufficient permissions for creating, destroying and modifying the relevant stack resources.

## Environment Settings
```
$ export STACKNAME=<Name of your stack>
$ export PROJECT=<The project name for resource cost tracking>
$ export LAMBDA=<The Arn of the Lambda that will receive new S3 Credentials>
$ export EDL_USERNAME=<A valid Earth Data Login user name>
$ export EDL_PASSWORD=<A valid Earth Data Login password>
```

## CDK Commands
### Synth
Display generated cloud formation template that will be used to deploy.
```
$ tox -e dev -r -- synth
```

### Diff
Display a diff of the current deployment and any changes created.
```
$ tox -e dev -r -- diff || true
```

### Deploy
Deploy current version of stack.
```
$ tox -e dev -r -- deploy
```

## Development
For active stack development run
```
$ tox -e dev -r -- version
```
This creates a local virtualenv in the directory `devenv`.  To use it for development
```
$ source devenv/bin/activate
```
Then run the following to install the project's pre-commit hooks
```
$ pre-commit install
```

## Tests
To run unit test for all included Lambda functions
```
tox -r
```
