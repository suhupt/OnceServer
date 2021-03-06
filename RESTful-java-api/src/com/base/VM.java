package com.base;

import java.io.UnsupportedEncodingException;
import java.net.MalformedURLException;
import java.net.URL;
import java.util.HashMap;
import java.util.Map;

import com.config.VMConfig;
import com.utils.CONST;
import com.utils.Connection;
import com.utils.Utils;

public class VM {
	private static final String urlString = "http://" + CONST.HOST + ":" + CONST.PORT + "/VMs/";
	
    /*******************************************
    Author: LHearen
    E-mail: LHearen@126.com
    Time  :	2015-12-03 16:19
    Description: according to the given parameters
    to create a VM in remote host;
     * @throws UnsupportedEncodingException 
    *******************************************/         
    public static void create(VMConfig config) throws MalformedURLException, UnsupportedEncodingException
    {
    	/*
    	 * used to post a VM configuration to server;
    	 * curl -X POST -H 'Content-Type: application/json'  http://133.133.135.13:5100/VM -d '{"uuid": "7504b4c5dd1543d6b469f701a4a3c3a8", "isoDir": "/home/res/iso/CentOS-7.1.iso", "diskDir": "/home/res/images/test1.qcow2", "bridgeSrc": "ovs0", "name": "vm", "memory": 1024, "vcpu": 2,"powerstate": "running"}'
    	 */
        Map<String, String> data = config.toMap();
        data.put("Module", "VM");
        data.put("Method", "create");
        String response = Connection.sendPost(urlString, data);
        System.out.println(response);
    }
    
    private static boolean sendMethod(String uuid, String methodName)
    {
    	return Utils.sendMethod(urlString, "VM", methodName, uuid);
    }
        
    /*******************************************
    Author      : LHearen
    E-mail      : LHearen@126.com
    Time        : 2015-12-15 16 : 09
    Description : Used to start a VM specified by uuid;
    *******************************************/
	public static boolean start(String uuidString)
	{
		return sendMethod(uuidString, "start");
	}
	
	public static boolean shutdown(String uuidString)
	{
		return sendMethod(uuidString, "shutdown");
	}

	public static boolean delete(String uuidString)
	{
		return sendMethod(uuidString, "delete");
	}
	
	public static boolean reboot(String uuidString)
	{
		return sendMethod(uuidString, "reboot");
	}
	
	public static boolean isTemplate(String uuidString)
	{
		return sendMethod(uuidString, "isTemplate");
	}
	
	public static boolean setTemplate(String uuidString)
	{
		return sendMethod(uuidString, "setTemplate");
	}
	
	public static boolean unsetTemplate(String uuidString)
	{
		return sendMethod(uuidString, "unsetTemplate");
	}
}
