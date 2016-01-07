import xml.etree.ElementTree as ET
from utils.Connection import Connection
from utils.OnceLogging import log, init
from utils.XmlConverter import XmlConverter
from utils.libvirt import libvirtError
from utils.DBHelper import VBDHelper
from utils.Tools import logNotFound

init("/var/log/xen/libvirt.log", "DEBUG", log)
conn = Connection.get_libvirt_connection()
PoolUUIDString = '27167fe7-fc9d-47d5-9cd0-717106ef67be'
VolumeUUIDString = '27167fe7-fc9d-47d5-9cd0-717106ef67be'


def createPool(_id, name, target):
    '''
    Author      : LHearen
    E-mail      : LHearen@126.com
    Time        : 2015-12-30 10 : 17
    Description : Using indispensible factors to create a pool;
    '''
    if len(_id) < 5:
        from utils.UUIDGenerator import createString
        global PoolUUIDString
        _id = createString()
    PoolUUIDString = _id
    config = XmlConverter.toSRXml(_id, name, target)
    try:
        conn.poolCreateXML(config)
    except libvirtError, e:
        log.debug("pool %s creation failed! Message: %s" % (name, e))
        return None
    return True

def deletePool(_id):
    '''
    Author      : LHearen
    E-mail      : LHearen@126.com
    Time        : 2015-12-30 10 : 17
    Description : Delete the pool specified by a name;
    '''
    try:
        pool = conn.storagePoolLookupByUUIDString(_id)
    except libvirtError, e:
        logNotFound("Pool", _id, e)
        return None
    if pool.isActive():
        pool.destroy()
    try:
        pool.undefine()
        filterDict = {"_id": _id}
        VBDHelper.removePool(filterDict)
    except libvirtError, e:
        log.debug("pool %s cannot be removed! Message: %s" % (_id, e))
        return None
    return True

def listPools():
    '''
    Author      : LHearen
    E-mail      : LHearen@126.com
    Time        : 2015-12-30 10 : 25
    Description : Used to list all known pools;
    '''
    try:
        poolNames = conn.listAllStoragePoolsNames()
    except libvirtError, e:
        log.debug("pool listing error! Message: %s" % e)
        return None
    if len(poolNames) > 0:
        return ','.join(poolNames)
    else:
        return ''

def createVolume(_id, poolName, volName, volSize):
    '''
    Author      : LHearen
    E-mail      : LHearen@126.com
    Time        : 2015-12-30 15 : 43
    Description : Create a volume in a existed pool specified by a pool name;
    '''
    if len(_id) < 5:
        from utils.UUIDGenerator import createString
        _id = createString()
    global VolumeUUIDString
    VolumeUUIDString = _id
    try:
        pool = conn.storagePoolLookupByName(poolName)
    except libvirtError, e:
        logNotFound("Pool", poolName, e)
        return None
    config = XmlConverter.toVolumeXml(volName, volSize)
    if not pool.isActive():
        pool.create()
    try:
        pool.createXML(config)
        return VolumeUUIDString
    except libvirtError, e:
        log.debug("Volume %s creation failed! Message: %s" % (volName, e))
        return None
    return None

def deleteVolume(_id, poolName, volName):
    '''
    Author      : LHearen
    E-mail      : LHearen@126.com
    Time        : 2015-12-30 10 : 31
    Description : Used to delete a volume in a specified pool;
    '''
    try:
        pool = conn.storagePoolLookupByName(poolName)
    except libvirtError, e:
        logNotFound("Pool", poolName, e)
        return None
    try:
        volume = pool.storageVolLookupByName(volName)
    except libvirtError, e:
        logNotFound("Volume", volName, e)
        return None
    try:
        volume.delete()
        filterDict = {"_id": _id}
        VBDHelper.removeVolume(filterDict)
    except libvirtError, e:
        log.debug("Volume %s deletion failed! Message: %s" % (volName, e))
        return None
    return True

def listVolumes(poolName):
    '''
    Author      : LHearen
    E-mail      : LHearen@126.com
    Time        : 2015-12-30 16:24
    Description : Used to list volume names in a pool;
    '''
    try:
        pool = conn.storagePoolLookupByName(poolName)
    except libvirtError, e:
        logNotFound("Pool", poolName, e)
        return None
    try:
        volumes = pool.listAllVolumes()
    except libvirtError, e:
        log.debug("%s pool.listAllVolumes method failed! Message: %s" % (poolName, e))
        return None
    volNames = ','.join([vol.name() for vol in volumes])
    return volNames
def attachVolume(vm_id, poolName, volName, target, driver='qemu', driverType='qcow2'):
    '''
    Author      : LHearen
    E-mail      : LHearen@126.com
    Time        : 2016-01-07 10:54
    Description : Attaching a volume to a VM;
    '''
    pool = None
    try:
        pool = conn.storagePoolLookupByName(poolName)
    except Exception, e:
        logNotFound("Pool", poolName, e)
        return None
    vol = None
    try:
        vol = pool.storageVolLookupByName(volName)
    except Exception, e:
        logNotFound("Volume", volName, e)
        return None
    root = ET.fromstring(vol.XMLDesc())
    volDir = root.find('key').text
    diskXmlConfig = XmlConverter.toDiskXml(volDir, target, driver, driverType)
    try:
        vm = conn.lookupByUUIDString(vm_id)
    except Exception, e:
        logNotFound("VM", vm_id, e)
        return None
    try:
        vm.attachDeviceFlags(diskXmlConfig)
    except Exception, e:
        log.debug("Attaching disk failed! Message: %s" % e)
        return None
    return True
