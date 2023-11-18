# Yaml templates for languages supported by memphis

## Go
```yaml
function_name: Example function
description: This is a description
tags:
  - tag: json
  - tag: go
  - tag: awesome
runtime: go1.19 
dependencies: go.mod
environment_vars:
  - name: SomeEnvVariable
    value: SomeValue
memory: 128
storage: 128
```

## Python
```yaml
function_name: Example function
description: This is a description
tags:
  - tag: json
  - tag: python
  - tag: awesome
runtime: python3.11 # python3.8 | python3.9 | python3.10 | python3.11 
dependencies: # ???
environment_vars:
  - name: SomeEnvVariable
    value: SomeValue
memory: 128
storage: 128
handler: event_handler
```

## JS
```yaml
function_name: Example function
description: This is a description
tags:
  - tag: json
  - tag: python
  - tag: awesome
runtime: nodejs18.x # nodejs14.x | nodejs16.x | nodejs18.x | nodejs20.x
dependencies: # ???
environment_vars:
  - name: SomeEnvVariable
    value: SomeValue
memory: 128
storage: 128
handler: eventHandler
```