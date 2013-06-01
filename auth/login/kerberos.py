#!/usr/bin/python

import getpass
import pexpect
import uuid
import ldap
import ldap.sasl
import os
import sys


def kerberos_destroy(exitstatus):
    kdestroy = os.system("/usr/bin/kdestroy")
    sys.exit(exitstatus or kdestroy)
def kerberos_login(user_id, password):
    ad_realm = "LOCAL.TJHSST.EDU"  # Active Directory Realm
    host = "iodine.tjhsst.edu"  # Active Directory Realm
    ldap_realm = "CSL.TJHSST.EDU"
    ldap_server = "ldap://iodine-ldap"
    cache = "/tmp/authtest-" + str(uuid.uuid4())

    base_dn = "dc=tjhsst,dc=edu"

    print("Cache file is " + cache)
    os.environ['KRB5CCNAME'] = cache

    kinit = pexpect.spawn("/usr/bin/kinit {}@{}".format(user_id, ad_realm))
    kinit.expect("{}@{}'s Password:".format(user_id, ad_realm))
    kinit.sendline(password)
    kinit.expect(pexpect.EOF)
    kinit.close()

    if(kinit.exitstatus == 0):
        print("Password correct")
        kgetcred = pexpect.spawn("/usr/bin/kgetcred ldap/{}@{}".format(host, ldap_realm))
        kgetcred.expect(pexpect.EOF)
        kgetcred.close()
        if(kgetcred.exitstatus == 0):
            print("Successfully authorized to LDAP service")

            # ldapsearch -h iodine-ldap -b'dc=tjhsst,dc=edu' iodineUid=2015elowman
            l = ldap.initialize(ldap_server)
            auth_tokens = ldap.sasl.gssapi()
            l.sasl_interactive_bind_s('', auth_tokens)
            print("Successfully bound to LDAP with " + l.whoami_s())
            filter = '(iodineUid=' + user_id + ')'
            # attrs = ['displayName']

            try:
                r = l.search_s(base_dn, ldap.SCOPE_SUBTREE, filter)[0][1]
            except IndexError:
                print("No user " + user_id + " found in LDAP")
                kerberos_destroy(1)

            name = r['cn'][0]
            print("\n" + name + "'s Schedule")
            print("-"*(len(name) + 11))

            courses = []
            for dn in r['enrolledclass']:
                try:
                    course = l.search_s(dn, ldap.SCOPE_SUBTREE)[0][1]
                    courses.append((course['classPeriod'][0], course['cn'][0], course['roomNumber'][0]))
                except IndexError:
                    "Course data incomplete"
                    kerberos_destroy(1)

            courses = sorted(courses, key=lambda x: x[0])
            for course in courses:
                print("Period {}: {}{}({})".format(course[0], course[1], " "*(25-len(course[1])), course[2]))
            kerberos_destroy(0)
        else:
            print("Authorization to LDAP failed")
            kerberos_destroy(1)
    else:
        print("Password incorrect")
        kerberos_destroy(1)

