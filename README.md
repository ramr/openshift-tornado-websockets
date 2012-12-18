Tornado (with Websockets) on Red Hat's OpenShift PaaS
=====================================================

Tornado running on OpenShift with Websocket support.

This git repository is a sample application to help you get started
with using Tornado on Red Hat's OpenShift PaaS.


Steps to get tornado running on OpenShift
-----------------------------------------

Create an account at http://openshift.redhat.com/

Create a namespace, if you haven't already do so

    rhc domain create -n <yournamespace>

Create a python-2.6 or a diy-0.1 application (you can name it anything via -a)

    rhc app create tornado python-2.6
         OR
    rhc app create tornado diy-0.1


Add this `github openshift-tornado-websockets` repository

    cd tornado
    git remote add upstream -m master git@github.com:ramr/openshift-tornado-websockets.git
    git pull -s recursive -X theirs upstream master
    
Then push the repo to OpenShift

    git push

That's it, you can now checkout your application on either of the
experimental websocket enabled ports:

    http://tornado-$yournamespace.rhcloud.com:8000
    OR
    https://tornado-$yournamespace.rhcloud.com:8443

