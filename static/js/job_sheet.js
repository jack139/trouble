
var study_count=0, job_count=0;
var option_xw = null,
	option_xwgj = null,
	option_xxxs = null,
	option_xl = null;

function add_study(){
	study_div = '<div id="study-'+study_count+'" class="bg-info" style="padding: 15px 0 1px 0;margin-bottom: 10px;">'+
		''+
		'    <div class="form-group">'+
		'        <label for="xl-'+study_count+'" class="col-sm-2 control-label">学历</label>'+
		'        <div class="col-sm-4">'+
		'            <select class="form-control" id="xl-'+study_count+'" name="xl-'+study_count+'">'+
		'                <option value="">--请选择--</option>'+ option_xl +
		'            </select>'+
		'        </div>'+
		'    </div>'+
		''+
		'    <div class="form-group">'+
		'        <label for="rxsj-'+study_count+'" class="col-sm-2 control-label">入学时间</label>'+
		'        <div class="col-sm-2">'+
		'            <input type="text" class="form-control" id="rxsj-'+study_count+'" name="rxsj-'+study_count+'" placeholder="" readonly="readonly" />'+
		'        </div>'+
		'        <label for="bysj-'+study_count+'" class="col-sm-2 control-label">毕业时间</label>'+
		'        <div class="col-sm-2">'+
		'            <input type="text" class="form-control" id="bysj-'+study_count+'" name="bysj-'+study_count+'" placeholder="" readonly="readonly" />'+
		'        </div>'+
		'    </div>'+
		''+
		'    <div class="form-group">'+
		'        <label for="byxx-'+study_count+'" class="col-sm-2 control-label">毕业学校</label>'+
		'        <div class="col-sm-6">'+
		'            <input type="text" class="form-control" id="byxx-'+study_count+'" name="byxx-'+study_count+'" placeholder="" />'+
		'        </div>'+
		'    </div>'+
		''+
		''+
		'    <div class="form-group">'+
		'        <label for="sxzy-'+study_count+'" class="col-sm-2 control-label">所学专业</label>'+
		'        <div class="col-sm-4">'+
		'            <input type="text" class="form-control" id="sxzy-'+study_count+'" name="sxzy-'+study_count+'" placeholder="" />'+
		'        </div>'+
		'    </div>'+
		''+
		''+
		'    <div class="form-group">'+
		'        <label for="xw-'+study_count+'" class="col-sm-2 control-label">学位</label>'+
		'        <div class="col-sm-4">'+
		'            <select class="form-control" id="xw-'+study_count+'" name="xw-'+study_count+'">'+
		'                <option value="">--请选择--</option>'+ option_xw +
		'            </select>'+
		'        </div>'+
		'    </div>'+
		''+
		''+
		'    <div class="form-group">'+
		'        <label for="zgxl-'+study_count+'" class="col-sm-2 control-label">是否最高学历</label>'+
		'        <div class="col-sm-2">'+
		'            <select class="form-control" id="zgxl-'+study_count+'" name="zgxl-'+study_count+'">'+
		'                <option value="">--请选择--</option>'+
		'                <option value="是">是</option>'+
		'                <option value="否">否</option>'+
		'            </select>'+
		'        </div>'+
		'    </div>'+
		''+
		''+
		'    <div class="form-group">'+
		'        <label for="xwsj-'+study_count+'" class="col-sm-2 control-label">（预计）学位获得时间</label>'+
		'        <div class="col-sm-2">'+
		'            <input type="text" class="form-control" id="xwsj-'+study_count+'" name="xwsj-'+study_count+'" placeholder="" readonly="readonly" />'+
		'        </div>'+
		'    </div>'+
		''+
		'    <div class="form-group">'+
		'        <label for="xwgj-'+study_count+'" class="col-sm-2 control-label">学位国家</label>'+
		'        <div class="col-sm-4">'+
		'            <select class="form-control" id="xwgj-'+study_count+'" name="xwgj-'+study_count+'">'+
		'                <option value="">--请选择--</option>'+ option_xwgj +
		'            </select>'+
		'        </div>'+
		'    </div>'+
		''+
		'    <div class="form-group">'+
		'        <label for="xxxs-'+study_count+'" class="col-sm-2 control-label">学习形式</label>'+
		'        <div class="col-sm-4">'+
		'            <select class="form-control" id="xxxs-'+study_count+'" name="xxxs-'+study_count+'">'+
		'                <option value="">--请选择--</option>'+ option_xxxs +
		'            </select>'+
		'        </div>'+
		'    </div>'+
		''+
		'    <div class="form-group">'+
		'        <label for="pylx-'+study_count+'" class="col-sm-2 control-label">培养类型</label>'+
		'        <div class="col-sm-4">'+
		'            <select class="form-control" id="pylx-'+study_count+'" name="pylx-'+study_count+'">'+
		'                <option value="">--请选择--</option>'+
		'                <option value="学术型">学术型</option>'+
		'                <option value="专业型">专业型</option>'+
		'            </select>'+
		'        </div>'+
		'    </div>'+
		''+
		''+
		'</div>';

	$("#study-list").prepend(study_div);

	/* 入学时间 */
	$('#rxsj-'+study_count).datetimepicker({
		format     : 'Y-m', 
		timepicker : false,
		maxDate:'+1970-01-01',
	});

	/* 毕业时间 */
	$('#bysj-'+study_count).datetimepicker({
		format     : 'Y-m', 
		timepicker : false,
		//maxDate:'+1970-01-01',
	});

	/* 学位时间 */
	$('#xwsj-'+study_count).datetimepicker({
		format     : 'Y-m', 
		timepicker : false,
		//maxDate:'+1970-01-01',
	});

	study_count++;
	$("#study_count").val(study_count);

}


function add_job(){
	job_div = '<div id="job-'+job_count+'" class="bg-info" style="padding: 15px 0 1px 0;margin-bottom: 10px;">'+
		''+
		'    <div class="form-group">'+
		'        <label for="kssj-'+job_count+'" class="col-sm-2 control-label">开始时间</label>'+
		'        <div class="col-sm-2">'+
		'            <input type="text" class="form-control" id="kssj-'+job_count+'" name="kssj-'+job_count+'" placeholder="" readonly="readonly" />'+
		'        </div>'+
		'        <label for="jssj-'+job_count+'" class="col-sm-2 control-label">结束时间</label>'+
		'        <div class="col-sm-2">'+
		'            <input type="text" class="form-control" id="jssj-'+job_count+'" name="jssj-'+job_count+'" placeholder="" readonly="readonly" />'+
		'        </div>'+
		'    </div>'+
		''+
		'    <div class="form-group">'+
		'        <label for="gzdw-'+job_count+'" class="col-sm-2 control-label">工作单位</label>'+
		'        <div class="col-sm-6">'+
		'            <input type="text" class="form-control" id="gzdw-'+job_count+'" name="gzdw-'+job_count+'" placeholder="" />'+
		'        </div>'+
		'    </div>'+
		''+
		'    <div class="form-group">'+
		'        <label for="szbm-'+job_count+'" class="col-sm-2 control-label">所在部门</label>'+
		'        <div class="col-sm-2">'+
		'            <input type="text" class="form-control" id="szbm-'+job_count+'" name="szbm-'+job_count+'" placeholder="" />'+
		'        </div>'+
		'        <label for="zyzw-'+job_count+'" class="col-sm-2 control-label">职业/职务</label>'+
		'        <div class="col-sm-2">'+
		'            <input type="text" class="form-control" id="zyzw-'+job_count+'" name="zyzw-'+job_count+'" placeholder="" />'+
		'        </div>'+
		'    </div>'+
		''+
		'    <div class="form-group">'+
		'        <label for="yydj-'+job_count+'" class="col-sm-2 control-label">医院等级</label>'+
		'        <div class="col-sm-4">'+
		'            <select class="form-control" id="yydj-'+job_count+'" name="yydj-'+job_count+'">'+
		'                <option value="">--请选择--</option>' +
		'                <option value="三级甲等">三级甲等</option>' +
		'                <option value="三级乙等">三级乙等</option>' +
		'                <option value="三级丙等">三级丙等</option>' +
		'                <option value="三级特等">三级特等</option>' +
		'                <option value="二级甲等">二级甲等</option>' +
		'                <option value="二级乙等">二级乙等</option>' +
		'                <option value="二级丙等">二级丙等</option>' +
		'                <option value="一级甲等">一级甲等</option>' +
		'                <option value="一级乙等">一级乙等</option>' +
		'                <option value="一级丙等">一级丙等</option>' +
		'                <option value="非医院等其他">非医院等其他</option>' +
		'            </select>'+
		'        </div>'+
		'    </div>'+
		''+
		''+
		'</div>';

	$("#job-list").prepend(job_div);

	/* 开始时间 */
	$('#kssj-'+job_count).datetimepicker({
		format     : 'Y-m-d', 
		timepicker : false,
		maxDate:'+1970-01-01',
	});

	/* 结束时间 */
	$('#jssj-'+job_count).datetimepicker({
		format     : 'Y-m-d', 
		timepicker : false,
		maxDate:'+1970-01-01',
	});

	job_count++;
	$("#job_count").val(job_count);

}


$(function(){
	$('#btn_add_study_list').click(function(){
		add_study();
	});

	$('#btn_add_job_list').click(function(){
		add_job();
	});

	$('#btn_search_gw').click(function(){
		var val = $("#gwbh").val().toUpperCase().trim();
		var opt = $('#sbgw option[value="'+val+'"]');

		if (val.length==0){
			alertify.warning("请输入岗位编号。");
		}
		else if (opt.length>0){
			$("#sbgw").val(val);
			$("#gwbh").val(val);
		}
		else{
			alertify.warning("未找到岗位编号对应的岗位，请确认编号是否正确。");
		}
	});

	$('#sbgw').change(function(){
		var val = $("#sbgw").val();
		$("#gwbh").val(val);
	});

	//$('#csrq').change(function(){
	//    var val = $("#csrq").val();
	//    var currentYear = (new Date).getFullYear();
	//    $("#nl").val(currentYear - val.split('-')[0]);
	//});

});


/*初始化时间控件*/
function date_init(){
	/* 出生日期 */
	$('#csrq').datetimepicker({
		format     : 'Y-m-d', 
		timepicker : false,
		maxDate:'+1970-01-01',
		onChangeDateTime:function(dp,$input){
			var val = $input.val();
			var currentYear = (new Date).getFullYear();

			$("#nl").val(currentYear - val.split('-')[0]);
			
		}
	});


	/* 现任党政管理职务时间 */
	$('#dzglsj').datetimepicker({
		format     : 'Y-m-d', 
		timepicker : false,
		maxDate:'+1970-01-01',
	});

	/* 导师资格聘任时间 */
	$('#dszgprsj').datetimepicker({
		format     : 'Y-m-d', 
		timepicker : false,
		maxDate:'+1970-01-01',
	});


	/* 现专业技术资格取得时间 */
	$('#zyjszgqdsj').datetimepicker({
		format     : 'Y-m-d', 
		timepicker : false,
		maxDate:'+1970-01-01',
	});

	/* 现专业技术职务聘任时间 */
	$('#xzyjszwprsj').datetimepicker({
		format     : 'Y-m-d', 
		timepicker : false,
		maxDate:'+1970-01-01',
	});

	/* 现教师系列专业技术职务任职时间 */
	$('#jsxlzyjsrzsj').datetimepicker({
		format     : 'Y-m-d', 
		timepicker : false,
		maxDate:'+1970-01-01',
	});

	/* 规培起始时间 */
	$('#gpqssj').datetimepicker({
		format     : 'Y-m-d', 
		timepicker : false,
		maxDate:'+1970-01-01',
	});

	/* 规培结束时间 */
	$('#gpjssj').datetimepicker({
		format     : 'Y-m-d', 
		timepicker : false,
		//maxDate:'+1970-01-01',
	});

	/* 规培证取得日期 */
	$('#gpzrq').datetimepicker({
		format     : 'Y-m-d', 
		timepicker : false,
		//maxDate:'+1970-01-01',
	});

	/* 首次参加工作日期 */
	$('#cjgzrq').datetimepicker({
		format     : 'Y-m-d', 
		timepicker : false,
		maxDate:'+1970-01-01',
	});


	/* 结/离婚日期 */
	$('#jhrq').datetimepicker({
		format     : 'Y-m-d', 
		timepicker : false,
		maxDate:'+1970-01-01',
	});
	
}



$(function(){
	$('#btn_submit').click(function(){
		var err = 0;
		var err_str = "";

		if ($("#must_ok").is(':checked')==false){
			err_str += "申请人承诺，";
			$("#must_box").css('border','1px solid red');
			err++;
		}

		var rylb=$("#rylb").val().trim();
		if (rylb.length==0){
			err_str += "人员类别，";
			$("#rylb").css('border','1px solid red');
			err++;
		}

		var gwlb = '';
/*
		var gwlb=$("#gwlb").val().trim();
		if (gwlb.length==0){
			err_str += "岗位类别，";
			$("#gwlb").css('border','1px solid red');
			err++;
		}
*/
		var zylb=$("#zylb").val().trim();
		if (zylb.length==0){
			err_str += "专业类别，";
			$("#zylb").css('border','1px solid red');
			err++;
		}

		var gwbh=$("#gwbh").val().trim();
		if (gwbh.length==0){
			err_str += "岗位编号，";
			$("#gwbh").css('border','1px solid red');
			err++;
		}

		var sbgw=$("#sbgw option:selected").text().trim();
		var sbgw2=$("#sbgw").val().trim();
		if (sbgw2.length==0){
			err_str += "申报岗位，";
			$("#sbgw").css('border','1px solid red');
			err++;
		}

		var xm  =$("#xm").val().trim();
		if (xm.length==0){
			err_str += "姓名，";
			$("#xm").css('border','1px solid red');
			err++;
		}

		var xb  =$("#xb").val().trim();
		if (xb.length==0){
			err_str += "性别，";
			$("#xb").css('border','1px solid red');
			err++;
		}

		var zjlx=$("#zjlx").val().trim();
		if (zjlx.length==0){
			err_str += "证件类型，";
			$("#zjlx").css('border','1px solid red');
			err++;
		}

		var zjhm=$("#zjhm").val().trim();
		if (zjhm.length==0){
			err_str += "证件号码，";
			$("#zjhm").css('border','1px solid red');
			err++;
		}

		var csrq=$("#csrq").val().trim();
		if (csrq.length==0){
			err_str += "出生日期，";
			$("#csrq").css('border','1px solid red');
			err++;
		}

		var nl  =$("#nl").val().trim();

		var mz  =$("#mz").val().trim();
		if (mz.length==0){
			err_str += "民族，";
			$("#mz").css('border','1px solid red');
			err++;
		}

		var zzmm=$("#zzmm").val().trim();
		if (zzmm.length==0){
			err_str += "政治面貌，";
			$("#zzmm").css('border','1px solid red');
			err++;
		}

		var gjdq=$("#gjdq").val().trim();
		if (gjdq.length==0){
			err_str += "国家/地区，";
			$("#gjdq").css('border','1px solid red');
			err++;
		}

		var jg_name=$("#jg_name").val().trim();
		var jg_code=$("#jg_code").val().trim();
		if (jg_code.length==0){
			err_str += "籍贯，";
			$("#prov0").css('border','1px solid red');
			$("#city0").css('border','1px solid red');
			$("#country0").css('border','1px solid red');
			err++;
		}

		var lxdh=$("#lxdh").val().trim();
		if (lxdh.length==0){
			err_str += "联系电话，";
			$("#lxdh").css('border','1px solid red');
			err++;
		}

		var lxyx=$("#lxyx").val().trim();
		if (lxyx.length==0){
			err_str += "联系邮箱，";
			$("#lxyx").css('border','1px solid red');
			err++;
		}

		var xgzdw=$("#xgzdw").val().trim();
		if (xgzdw.length==0){
			err_str += "现工作单位，";
			$("#xgzdw").css('border','1px solid red');
			err++;
		}


		var dzglzw=$("#dzglzw").val().trim();
		var dzglsj=$("#dzglsj").val().trim();

		var gzyydj=$("#gzyydj").val().trim();
		if (gzyydj.length==0){
			err_str += "现工作医院等级，";
			$("#gzyydj").css('border','1px solid red');
			err++;
		}

		var sjyygzsj=$("#sjyygzsj").val().trim();
		if (sjyygzsj.length==0){
			err_str += "三甲医院工作时间，";
			$("#sjyygzsj").css('border','1px solid red');
			err++;
		}

		var cgjl=$("#cgjl").val().trim();
		var kyxm=$("#kyxm").val().trim();
		var xsjz=$("#xsjz").val().trim();
		var poxm=$("#poxm").val().trim();
		var podw=$("#podw").val().trim();
		var pozw=$("#pozw").val().trim();

		var hjqk=$("#hjqk").val().trim();
		var cykyxmqk=$("#cykyxmqk").val().trim();
		var lwlzqk=$("#lwlzqk").val().trim();
		var xsttrzqk=$("#xsttrzqk").val().trim();
		var lczyyj=$("#lczyyj").val().trim();
		var qtcg=$("#qtcg").val().trim();
		var pozgxl=$("#pozgxl").val().trim();
		var pozgxw=$("#pozgxw").val().trim();

		var yjsdszg=$("#yjsdszg").val().trim();
		if (yjsdszg.length==0){
			err_str += "研究生导师资格，";
			$("#yjsdszg").css('border','1px solid red');
			err++;
		}

		var dszgprsj=$("#dszgprsj").val().trim();
		//if (yjsdszg!="无" && dszgprsj.length==0){
		//	err_str += "导师资格聘任时间，";
		//	$("#dszgprsj").css('border','1px solid red');
		//	err++;
		//}

		var zyjszg=$("#zyjszg").val().trim();
		if (zyjszg.length==0){
			err_str += "现专业技术资格，";
			$("#zyjszg").css('border','1px solid red');
			err++;
		}

		var zyjszgqdsj=$("#zyjszgqdsj").val().trim();
		//if (zyjszg.substr(0,4)!="1001" && zyjszg.substr(0,4)!="1101" && zyjszgqdsj.length==0){
		//	err_str += "现专业技术资格取得时间，";
		//	$("#zyjszgqdsj").css('border','1px solid red');
		//	err++;
		//}

		var zyjszgzymc=$("#zyjszgzymc").val().trim();
		//if (zyjszg.substr(0,4)!="1101" && zyjszgzymc.length==0){
		//	err_str += "现专业技术资格专业名称，";
		//	$("#zyjszgzymc").css('border','1px solid red');
		//	err++;
		//}

		var xzdj=$("#xzdj").val().trim();
		if (xzdj.length==0){
			err_str += "专技职务/行政等级，";
			$("#xzdj").css('border','1px solid red');
			err++;
		}

		var xspzyjszw=$("#xspzyjszw").val().trim();
		if (xspzyjszw.length==0){
			err_str += "现受聘专业技术职务，";
			$("#xspzyjszw").css('border','1px solid red');
			err++;
		}

		var xzyjszwprsj=$("#xzyjszwprsj").val().trim();
		//if (xspzyjszw.substr(0,4)!="1001" && xspzyjszw.substr(0,4)!="1101" && xzyjszwprsj.length==0){
		//	err_str += "现专业技术职务聘任时间，";
		//	$("#xzyjszwprsj").css('border','1px solid red');
		//	err++;
		//}

		var xzyjszwprmc=$("#xzyjszwprmc").val().trim();
		//if (xspzyjszw.substr(0,4)!="1101" && xzyjszwprmc.length==0){
		//	err_str += "现专业技术职务聘任专业名称，";
		//	$("#xzyjszwprmc").css('border','1px solid red');
		//	err++;
		//}

		var zhiylb=$("#zhiylb").val().trim();
		var zhiyfw=$("#zhiyfw").val().trim();
		var jsxlzyjsxx=$("#jsxlzyjsxx").val().trim();
		var jsxlzyjszw=$("#jsxlzyjszw").val().trim();
		var jsxlzyjsrzsj=$("#jsxlzyjsrzsj").val().trim();

		var gpqk=$("#gpqk").val().trim();
		if (gpqk.length==0){
			err_str += "规培情况，";
			$("#gpqk").css('border','1px solid red');
			err++;
		}

		//var gpnx=$("#gpnx").val().trim();
		var gpdw=$("#gpdw").val().trim();
		var gpqssj=$("#gpqssj").val().trim();
		var gpjssj=$("#gpjssj").val().trim();
		var gpzy=$("#gpzy").val().trim();
		var gphg=$("#gphg").val().trim();
		var gpzrq=$("#gpzrq").val().trim();

		var sglm=$("#sglm").val().trim();
		if (sglm.length==0){
			err_str += "身高，";
			$("#sglm").css('border','1px solid red');
			err++;
		}

		var yysp=$("#yysp").val().trim();
		if (yysp.length==0){
			err_str += "英语水平，";
			$("#yysp").css('border','1px solid red');
			err++;
		}

		var cjgzrq=$("#cjgzrq").val().trim();
		/*
		if (cjgzrq.length==0){
			err_str += "参加工作时间，";
			$("#cjgzrq").css('border','1px solid red');
			err++;
		}
		*/

		var hjdz_name=$("#hjdz_name").val().trim();
		var hjdz_code=$("#hjdz_code").val().trim();
		if (hjdz_code.length==0){
			err_str += "户籍地址，";
			$("#prov1").css('border','1px solid red');
			$("#city1").css('border','1px solid red');
			$("#country1").css('border','1px solid red');
			err++;
		}


		var hjxz=$("#hjxz").val().trim();
		if (hjxz.length==0){
			err_str += "输入户籍性质，";
			$("#hjxz").css('border','1px solid red');
			err++;
		}

		var jkzk=$("#jkzk").val().trim();
		if (jkzk.length==0){
			err_str += "健康状况，";
			$("#jkzk").css('border','1px solid red');
			err++;
		}

		var hyzk=$("#hyzk").val().trim();
		if (hyzk.length==0){
			err_str += "婚姻状况，";
			$("#hyzk").css('border','1px solid red');
			err++;
		}

		var jhrq=$("#jhrq").val().trim();
		if (hyzk!="未婚" && jhrq.length==0){
			err_str += "结/离婚日期，";
			$("#jhrq").css('border','1px solid red');
			err++;
		}

		var syzn=$("#syzn").val().trim();
		if (syzn.length==0){
			err_str += "生育子女，";
			$("#syzn").css('border','1px solid red');
			err++;
		}

		var qtbz=$("#qtbz").val().trim();

		if (study_count==0){
			err_str += "学习经历。";
			err++;
		}

		if (err>0) {
			alertify.warning("请输入必填项信息（红色标记部分）: "+err_str);
			return;
		}

		var image=$("#form_image").val();

		var study_list = [];
		if (study_count>0){
			for (i=0;i<study_count;i++){
				study_list[i] = {
					'xl'   : $("#xl-"+i).val().trim(),
					'rxsj' : $("#rxsj-"+i).val().trim(),
					'bysj' : $("#bysj-"+i).val().trim(),
					'byxx' : $("#byxx-"+i).val().trim(),
					'zgxl' : $("#zgxl-"+i).val().trim(),
					'sxzy' : $("#sxzy-"+i).val().trim(),
					'xw'   : $("#xw-"+i).val().trim(),
					'xwsj' : $("#xwsj-"+i).val().trim(),
					'xwgj' : $("#xwgj-"+i).val().trim(),
					'xxxs' : $("#xxxs-"+i).val().trim(),
					'pylx' : $("#pylx-"+i).val().trim(),
				}
			}
		}

		var job_list = [];
		if (job_count>0){
			for (i=0;i<job_count;i++){
				job_list[i] = {
					'kssj' : $("#kssj-"+i).val().trim(),
					'jssj' : $("#jssj-"+i).val().trim(),
					'gzdw' : $("#gzdw-"+i).val().trim(),
					'szbm' : $("#szbm-"+i).val().trim(),
					'zyzw' : $("#zyzw-"+i).val().trim(),
					'yydj' : $("#yydj-"+i).val().trim(),
				}
			}
		}


		$("#wait_gif").show();


		alertify.confirm("请确认：", "应聘信息表提交后将不能修改，确认要提交吗？",
			function(){
				$.ajax({
					type: "POST",
					url: "/job/sheet",
					async: true,
					timeout: 15000,
					data: {rylb:rylb,gwlb:gwlb,zylb:zylb,gwbh:gwbh,
						sbgw:sbgw,xm:xm,xb:xb,zjlx:zjlx,zjhm:zjhm,
						csrq:csrq,nl:nl,mz:mz,zzmm:zzmm,gjdq:gjdq,jg_name:jg_name,jg_code:jg_code,
						lxdh:lxdh,lxyx:lxyx,xgzdw:xgzdw,gzyydj:gzyydj,
						sjyygzsj:sjyygzsj,cgjl:cgjl,kyxm:kyxm,xsjz:xsjz,podw:podw,pozw:pozw,
						hjqk:hjqk,cykyxmqk:cykyxmqk,lwlzqk:lwlzqk,qtcg:qtcg,pozgxl:pozgxl,pozgxw:pozgxw,xsttrzqk:xsttrzqk,lczyyj:lczyyj,
						yjsdszg:yjsdszg,dszgprsj:dszgprsj,zyjszg:zyjszg,zyjszgqdsj:zyjszgqdsj,xzdj:xzdj,gpqk:gpqk,
						gpzrq:gpzrq,sglm:sglm,yysp:yysp,cjgzrq:cjgzrq,hjdz_code:hjdz_code,hjdz_name:hjdz_name,
						hjxz:hjxz,jkzk:jkzk,
						hyzk:hyzk,jhrq:jhrq,syzn:syzn,qtbz:qtbz,study_list:JSON.stringify(study_list),
						dzglzw:dzglzw,dzglsj:dzglsj,poxm:poxm,zyjszgzymc:zyjszgzymc,xspzyjszw:xspzyjszw,
						xzyjszwprsj:xzyjszwprsj,xzyjszwprmc:xzyjszwprmc,zhiylb:zhiylb,zhiyfw:zhiyfw,
						jsxlzyjsxx:jsxlzyjsxx,jsxlzyjszw:jsxlzyjszw,jsxlzyjsrzsj:jsxlzyjsrzsj,gpdw:gpdw,
						gpqssj:gpqssj,gpjssj:gpjssj,gpzy:gpzy,gphg:gphg,image:image,
						job_list:JSON.stringify(job_list)},
					dataType: "json",
					complete: function(xhr, textStatus)
					{
						if(xhr.status==200){
							var retJson = JSON.parse(xhr.responseText);
							if (retJson["ret"]==0){
								$("#block2").hide();
								$("#alert2").show();
								$("#wait_gif").hide();
								alertify.alert("提交成功",retJson["msg"], function(){
									window.location.replace('/job/sheet');
								});
							}
							else{
								$("#alert2_text").text(retJson["msg"]);
								alertify.error(retJson["msg"]);
							}
						}
						else{
							alertify.error("网络异常！请稍后再试");
						}
					}
				});

			},
			function(){
			}
		);

	});
});

