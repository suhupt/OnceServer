from utils.Connection import Connection
from utils.OnceLogging import log, init
from utils.XmlConverter import XmlConverter
from time import sleep
from utils.DBHelper import VMHelper
from utils.UUIDGenerator import createString
from utils.Tools import logNotFound

init("/var/log/xen/libvirt.log", "DEBUG", log)
conn = Connection.get_libvirt_connection()
UUIDString = '27167fe7-fc9d-47d5-9cd0-717106ef67be'
Name = 'vm'

def create(_id, name, memory, vcpu, mac, diskDir, isoDir, bridgeSrc):
    '''
    Author      : LHearen
    E-mail      : LHearen@126.com
    Time        : 2015-12-16 09 : 43
    Description : Using limited parameters to create a VM and return its UUIDString;
    '''
    uuid = _id
    if len(uuid) < 5:
        uuid = createString()
    name = name if name else uuid
    global UUIDString
    UUIDString = uuid
    global Name
    Name = name
    hvm = {"loader": "/usr/lib/xen/boot/hvmloader"}
    hvm["boot"] = "cdrom"
    hvm["device_model"] = "/usr/lib/xen/bin/qemu-system-i386"
    image = {"hvm": hvm}

    tap2 = {"dev": "hdc:cdrom"}
    tap2["uname"] = "tap:aio:" + isoDir
    tap2["mode"] = "r"

    vif = {"bridge": bridgeSrc}
    if mac is not None:
        vif["mac"] = mac;

    vbd = {"dev": "hda:disk"}
    vbd["uname"] = "tap:aio:" + diskDir
    vbd["mode"] = "w"

    vfb = {"location": "0.0.0.0:5900"}
    vfb["vnclisten"] = "0.0.0.0"

    console = {"location": "0"}
    xmlConfig = XmlConverter.toVMXml(uuid, name, memory, vcpu, image, tap2,
                                        vif, vbd, vfb, console)
    # print xmlConfig
    return define_VM_by_xml(xmlConfig)


def define_VM_by_xml(xml_config):
    '''
    added by LHearen
    E-mail: LHearen@126.com
    Used to define a VM by a xml configuration file, dump its
    automatically generated internal xml configuration file and
    initialize the extra configuration file for latter use.
    '''
    # log.debug(xml_config)
    # log.error(xml_config)
    try:
        dom = conn.defineXML(xml_config)
    except Exception:
        log.error("VM creation failed!")
        return None
    return dom.UUIDString()


def start(_id, flags=0):
    '''
    Author      : LHearen
    E-mail      : LHearen@126.com
    Time        : 2015-12-15 15 : 44
    Description : Used to start the VM pointed by uuid;
    '''
    dom = conn.lookupByUUIDString(_id)
    try:
        dom.createWithFlags(int(flags))
    except Exception, e:
        log.error("Started dom %s failed! Message: %s" % (_id, e))
        return None
    else:
        return True

def shutdown(_id, flags=0):
    '''
    Author      : LHearen
    E-mail      : LHearen@126.com
    Time        : 2015-12-16 13 : 49
    Description : Shutdown the VM specified by uuid
                if it cannot shutdown as usual, destroy it after a certain delay;
    '''
    delay = 3
    dom = conn.lookupByUUIDString(_id)
    if dom:
        try:
            dom.shutdownFlags(int(flags))
            while delay > 0:
                sleep(1)
                if not dom.isActive(): return True
                delay -= 1
            if dom.isActive():
                dom.destroyFlags(int(flags))
            if not dom.isActive(): return True
        except Exception, e:
            log.error("VM %s shutdown failed! Message: %s" % (_id, e))
    return None

def delete(_id, flags=0):
    '''
    Author      : LHearen
    E-mail      : LHearen@126.com
    Time        : 2015-12-16 14 : 00
    Description : destory the VM first if it's still active
                and then undefine it and delete the document in db;
    '''
    dom = None
    try:
        dom = conn.lookupByUUIDString(_id)
    except Exception, e:
        logNotFound("VM", _id, e)
        return None
    if dom:
        if dom.isActive(): dom.destroyFlags(int(flags))
        try:
            dom.undefineFlags(int(flags))
        except Exception, e:
            log.debug("VM %s deletion failed! Message: %s" % (_id, e))
        try:
            conn.lookupByUUIDString(_id)
        except Exception, e:
            log.error("VM %s deletion failed! Message: %s" % (_id, e))
            filterDict = {"_id": _id}
            ret = VMHelper.remove(filterDict)
            if ret['ok'] > 0:
                return True
            else:
                log.debug("mongodb deletion failed!")
                return None
    return None

def reboot(_id, flags=0):
    '''
    Author      : LHearen
    E-mail      : LHearen@126.com
    Time        : 2015-12-16 14 : 00
    Description : waiting for a period of time until vm is off,
                after which destroy it and then start it;
    '''
    unit = 2
    dom = None
    try:
        dom = conn.lookupByUUIDString(_id)
    except Exception:
        logNotFound("VM", _id, e)
        return None
    try:
        dom.shutdownFlags(int(flags))
    except:
        pass
    for i in range(3):
        sleep(unit)
        if not dom.isActive():
            break;
    if dom.isActive():
        try:
            dom.destroy()
        except:
            pass
    if not dom.isActive():
        try:
            dom.createWithFlags(int(flags))
        except:
            pass
    else: return None
    if not dom.isActive(): return None
    else: return True

def setTemplate(_id):
    '''
    Author      : LHearen
    E-mail      : LHearen@126.com
    Time        : 2016-01-06 14:02
    Description : Used to set the VM specified by _id template;
    '''
    ret = VMHelper.update({"_id": _id}, {"isTemplate": True})
    if ret['ok'] > 0:
        return True
    return None

def unsetTemplate(_id):
    '''
    Author      : LHearen
    E-mail      : LHearen@126.com
    Time        : 2016-01-06 14:02
    Description : Used to set the VM specified by _id not template;
    '''
    ret = VMHelper.update({"_id": _id}, {"isTemplate": False})
    if ret['ok'] > 0:
        return True
    return None

def isTemplate(_id):
    '''
    Author      : LHearen
    E-mail      : LHearen@126.com
    Time        : 2015-12-17 11 : 20
    Description : Used to retrieve the isTemplate attribute from DB;
    '''
    print "inside isTemplate ****************"
    ret = VMHelper.retrieve({"_id": _id})["isTemplate"]
    if str(ret).lower() == 'false':
        return False
    else: return True
