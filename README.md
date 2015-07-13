# sublime-vm4docker
automatic file touch on OS X for docker vm

This is made for [vm4docker](https://github.com/yvess/vm4docker), this
should also work with boot2docker.

## Requirements

A host named `docker` should exits, or you can change it with the `host` settings.
You should be able to ssh to your docker host under the current user.

In your docker vm the `/Users` folder from you mac should be mounted
(nfs, shared folders, etc). 

## What It Does

The plugin does a ssh to the docker vm and does a
touch of the same file path you are editing in your mac.

This is useful for auto reloading development setups in you docker vm, which
listen on ionotify, for example flask oder django dev servers.

## Setttings

```json
{
    "host": "docker",
    "file_extensions": ["py", "md"],
    "do_ssh_key_checking": false,
    "watch_paths": ["/Users/myuser/myprojects", "/Users/myuser/otherprojects"]
}
```

- host: default: "docker", "mydockerhost", ssh host
- file_extenions:  default: [] (all), ["py", "md"], only trigger with this file extensions
- watch_paths: default: $HOME, ["/Users/myuser/myprojects", "/Users/myuser/otherprojects"],
  only trigger if file is in one of this paths, the path must be inside `/Users`
- do_ssh_key_checking: default: `false`, `true|false`, force ssh key checking with `true`
