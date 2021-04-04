# This repo is no more maintained
I've lost hope in Aruba Cloud ability to advance its API long ago,  
and after price hike of the 1€ VMs announced 2020-07-01,  
thier service offering became less interesting for me than Hetzner's.  

# Misc ArubaCloud API tryouts

In order of appearance:

1. attic/PyArubaAPI - using official Python API.
1. aruba.py - same JSON endpoints, using 'requests'.
1. ArubaCloud.java - WS-API.
1. try-zeep.py - WS-API

# (in)security notice
this repo has a bit hidden copy of ancient code of Aruba's open-source example of VM control panel.
As this code is old as hell, it has lots of vulnerable dependancies to say the least.
As of 2021-04-04 the list served by Github is (only  in `attic/java-openpanel-code-0-r15-trunk/pom.xml`)
* dom4j:dom4j **high severity** 2020-07-21
* org.springframework.security:spring-security-core **high severity** 2020-06-15
* commons-beanutils:commons-beanutils **high severity** 2020-06-11
* org.codehaus.jackson:jackson-mapper-asl **high severity** 2020-02-05
* log4j:log4j _moderate severity_ 2020-01-07
