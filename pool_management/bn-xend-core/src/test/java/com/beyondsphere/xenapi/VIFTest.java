package com.beyondsphere.xenapi;

import java.net.MalformedURLException;
import java.util.Map;
import java.util.Set;

import org.apache.xmlrpc.XmlRpcException;

import com.beyondsphere.xenapi.Connection;
import com.beyondsphere.xenapi.VIF;
import com.beyondsphere.xenapi.VM;
import com.beyondsphere.xenapi.Types.BadServerResponse;
import com.beyondsphere.xenapi.Types.SessionAuthenticationFailed;
import com.beyondsphere.xenapi.Types.XenAPIException;

public class VIFTest {

	/**
	 * @param args
	 * @throws XmlRpcException 
	 * @throws XenAPIException 
	 * @throws MalformedURLException 
	 * @throws SessionAuthenticationFailed 
	 * @throws BadServerResponse 
	 */
	public static void main(String[] args) throws BadServerResponse, SessionAuthenticationFailed, MalformedURLException, XenAPIException, XmlRpcException {
		Connection c = new Connection("http://133.133.135.8:9363", "root",
				"onceas");
		/*************获取VIF对象********/
		VM vm = VM.getByNameLabel(c, "CentOS_6.3_ceph_zfs").iterator().next();
		VIF vif = vm.getVIFs(c).iterator().next();
//		System.out.println(vif);
		/*************获取VIF对象的record值********/
//		VIF.Record record = vif.getRecord(c);
//		System.out.println(record);
//		VIF vif = VIF.getByUuid(c, uuid)
		/*************通过record值创建VIF对象********/
//		VIF vif_create = VIF.create(c, record);
		/*************通过record和host值创建VIF对象********/
//		Host host = Host.getByUuid(c, "b37b888e-f069-c075-cbe1-4326d08b538d");
//		VIF vif_createOn = VIF.createOn(c, record, host);
		/*************删除指定的VIF对象********/
//		vif.destroy(c);
		/*************获取指定的VIF对象的uuid值********/
//		String uuid = vif.getUuid(c);
//		System.out.println(uuid);
		/*************获取指定的VIF对象的allowed_operations域********/
//		Set<Types.VifOperations> allowed_operations = vif.getAllowedOperations(c);
//		System.out.println(allowed_operations);
		/*************获取指定的VIF对象的current_operations域********/
//		Map<String, Types.VifOperations> current_operations = vif.getCurrentOperations(c);
//		System.out.println(current_operations); 
		/*************获取指定的VIF对象的device域********/
//		String device = vif.getDevice(c);
//		System.out.println(device);
		/*************获取指定的VIF对象的network域********/
//		Network network = vif.getNetwork(c);
//		System.out.println(network);
		/*************获取指定的VIF对象的vm域********/
//		VM vm_temp = vif.getVM(c);
//		System.out.println(vm_temp);
		/*************获取指定的VIF对象的MAC域********/
//		String MAC = vif.getMAC(c);
//		System.out.println(MAC);
		/*************获取指定的VIF对象的MTU域********/
//		Long MTU = vif.getMTU(c);
//		System.out.println(MTU);
		/*************(不支持)获取指定的VIF对象的other_config域********/
//		Map<String, String> other_config = vif.getOtherConfig(c);
//		System.out.println(other_config);
		/*************(不支持)获取指定的VIF对象的currently_attached域********/
//		Boolean currently_attached = vif.getCurrentlyAttached(c);
//		System.out.println(currently_attached);
		/*************(不支持)获取指定的VIF对象的status_code域********/
//		Long status_code = vif.getStatusCode(c);
//		System.out.println(status_code);
		/*************(不支持)获取指定的VIF对象的status_detail域********/
//		String status_detail = vif.getStatusDetail(c);
//		System.out.println(status_detail);
		/*************获取指定的VIF对象的runtime_properties域********/
//		Map<String, String> runtime_properties = vif.getRuntimeProperties(c);
//		System.out.println(runtime_properties);
		/*************(不支持)获取指定的VIF对象的algorithm_type域********/
//		String algorithm_type = vif.getQosAlgorithmType(c);
//		System.out.println(algorithm_type);
		/*************(不支持)获取指定的VIF对象的algorithm_params域********/
//		Map<String, String> algorithm_params = vif.getQosAlgorithmParams(c);
//		System.out.println(algorithm_params);
		/*************(不支持)获取指定的VIF对象的supported_algorithms域********/
//		Set<String> supported_algorithms = vif.getQosSupportedAlgorithms(c);
//		System.out.println(supported_algorithms); 
		/*************获取指定的VIF对象的metrics域********/
//		VIFMetrics metrics = vif.getMetrics(c);
//		System.out.println(metrics);  
		/*************(不支持)获取指定的VIF对象的MAC_autogenerated域********/
//		Boolean MAC_autogenerated = vif.getMACAutogenerated(c);
//		System.out.println(MAC_autogenerated);   
		/*************(不支持)获取指定的VIF对象的other_config域********/
//		Map<String, String> other_config = null;
//		vif.setOtherConfig(c, other_config);
		/*************(不支持)为指定VIF对象的other_config域增加key,value对********/
//		String key = "";
//		String value = "";
//		vif.addToOtherConfig(c, key, value);		
		/*************(不支持)从指定VIF对象的other_config域中删除key,value对********/ 
//		String key = "";
//		vif.removeFromOtherConfig(c, key);
		/*************(不支持)设置指定VIF对象的algorithm_type域********/ 
//		String algorithm_type = null;
//		vif.setQosAlgorithmType(c, algorithm_type);
		/*************(不支持)设置指定VIF对象的algorithm_params域********/ 
//		Map<String, String> algorithmParams = null;
//		vif.setQosAlgorithmParams(c, algorithmParams);
		/*************(不支持)为指定VIF对象的algorithm_params域增加key,value对********/ 
//		String key = null;
//		String value = null;
//		vif.addToQosAlgorithmParams(c, key, value);
		/*************(不支持)从指定VIF对象的algorithm_params域中删除key,value对********/ 
//		String key = null;
//		vif.removeFromQosAlgorithmParams(c, key);
		/*************(不支持)********/
//		vif.plug(c);
		/*************(不支持)********/
//		vif.unplug(c);
		/*************获取当前所有的VIF集合********/
//		Set<VIF> vbd_set = VIF.getAll(c);
//		System.out.println(vbd_set);
		/*************获取当前所有的VIF集合********/
//		Map<VIF, VIF.Record> map = VIF.getAllRecords(c);
//		System.out.println(map);
	}

}
