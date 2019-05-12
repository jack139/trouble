var prov=[];
var city=[];
var country=[];
var current=[];

function init_city(){
    prov[0] = $('#prov0')[0];
    city[0] = $('#city0')[0];
    country[0] = $('#country0')[0];

    prov[1] = $('#prov1')[0];
    city[1] = $('#city1')[0];
    country[1] = $('#country1')[0];


    /*用于保存当前所选的省市区*/
    current[0] = {
        prov: '',
        city: '',
        country: ''
    };

    current[1] = {
        prov: '',
        city: '',
        country: ''
    };


    /*自动加载省份列表*/
    (function showProv() {
        var len = provice.length;
        for (var i = 0; i < len; i++) {
            var provOpt0 = document.createElement('option');
            var provOpt1 = document.createElement('option');
            provOpt0.innerText = provice[i]['name'];
            provOpt0.value = i;
            prov[0].appendChild(provOpt0);

            provOpt1.innerText = provice[i]['name'];
            provOpt1.value = i;
            prov[1].appendChild(provOpt1);
        }
    })();

}


/*根据所选的省份来显示城市列表*/
function showCity(obj, cid) {
    var val = obj.options[obj.selectedIndex].value;
    if (val != current[cid].prov) {
        current[cid].prov = val;
    }
    console.log(val);
    if (val!=null) {
        city[cid].length = 1;
        country[cid].length = 1; 
        if (val!=''){
            var cityLen = provice[val]["city"].length;
            for (var j = 0; j < cityLen; j++) {
                var cityOpt = document.createElement('option');
                cityOpt.innerText = provice[val]["city"][j].name;
                cityOpt.value = j;
                city[cid].appendChild(cityOpt);
            }
        }
    }
}

/*根据所选的城市来显示县区列表*/
function showCountry(obj, cid) {
    var val = obj.options[obj.selectedIndex].value;
    current[cid].city = val;
    if (val!=null) {
        country[cid].length = 1; //清空之前的内容只留第一个默认选项
        if (val!=''){
            var countryLen = provice[current[cid].prov]["city"][val].county.length;
            for (var n = 0; n < countryLen; n++) {
                var countryOpt = document.createElement('option');
                countryOpt.innerText = provice[current[cid].prov]["city"][val].county[n][1];
                countryOpt.value = n;
                country[cid].appendChild(countryOpt);
            }
        }
    }
}

/*选择县区之后的处理函数*/
function selecCountry(obj,cid) {
    current[cid].country = obj.options[obj.selectedIndex].value;
    if ((current[cid].city != null) && (current[cid].country != null)) {
        var id_name="#jg";
        if (cid==1) id_name="#hjdz";

        $(id_name+"_name").val(provice[current[cid].prov].name + provice[current[cid].prov]["city"][current[cid].city].name + 
            provice[current[cid].prov]["city"][current[cid].city].county[current[cid].country][1]);
        $(id_name+"_code").val(provice[current[cid].prov]["city"][current[cid].city].county[current[cid].country][0]);
    }
}

