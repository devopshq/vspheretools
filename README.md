# vspheretools

[![vspheretools code quality](https://api.codacy.com/project/badge/Grade/185f7c8a13c84f88bf8b93280e457ffc)](https://www.codacy.com/app/tim55667757/vspheretools/dashboard)

Home wiki-page: https://github.com/devopshq/vspheretools/wiki/vSphereTools-Instruction-(ru)


## How to use vspheretools-metarunners
* Install (or copy) xml metarunners on your TeamCity admin page: https://[teamcity_server]/admin/editProject.html?projectId=_Root&tab=metaRunner (Administration - Root project - Meta-Runners)
* Create new VCS from vspheretools project: https://github.com/devopshq/vspheretools
* Attach new VCS to your TeamCity project and set up checkout rules: 
+:.=>%default_devops_tools_path_local%/vspheretools
* Create variable default_devops_tools_path_local in your TeamCity project and set value, e.g. "devops-tools". It is local path for devops-tools repository.

See also wiki-page: https://github.com/devopshq/vspheretools/wiki/vSphereTools-Instruction-(ru)
