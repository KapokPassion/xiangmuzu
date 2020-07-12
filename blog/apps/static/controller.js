function get_l1(){
    $.ajax({
        url:"/l1"
        success:function(data){
            l1_Option.series[0].data = [15, 20, 36, 10, 10, 20]
            l1.setOption(l1_Option)

        },
        error:function(){
        }
    }
    )
}
get_l1()