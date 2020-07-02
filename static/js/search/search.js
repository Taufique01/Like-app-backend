var Zillow = (function () {
    ////private variable
    var zillow;
    var index;
  
    return {
        set: function (datas) {
            zillow = datas;
            index=0;

        },
        setIndex: function (i) {
            
           index=index+i;
           if(index<0)
              index=zillow.length-1;
           else if(index>=zillow.length)
              index=0;

        },
        getIndex: function () {
            
           return index;

        },
        datas: function () {

            return zillow;
        }

    };
})();


function getValidValue(value){

  if(value)
     return value
   return "....."

} 

function updateZillowView(){
  
    var index=Zillow.getIndex();
    var zillow=Zillow.datas()[index]
    var temp=index+1;
    $("#z-index").html(""+temp);
  
    $("#table-address").html(zillow.address.street);
    $("#table-city").html(zillow.address.city);
    $("#table-state").html(zillow.address.state);
    $("#table-zip").html(zillow.address.zipcode);
    $("#table-lat").html(zillow.address.latitude);
    $("#table-long").html(zillow.address.longitude);

    $("#a-home-details").attr("href",zillow.links.home_details);
    $("#iframe-home-details").attr("src",zillow.links.home_details);
    $("#a-map").attr("href",zillow.links.map_this_home);
    $("#iframe-map").attr("src",zillow.links.map_this_home);
    $("#a-similars").attr("href",zillow.links.similar_sales);
    ////class for zestimate
    
    $(".table-zestimate").html(getValidValue(zillow.zestimate.zestimate));
    
    $(".table-updated").html(getValidValue(zillow.zestimate.last_updated));
    $(".table-val-change").html(getValidValue(zillow.zestimate.value_change));
    $(".table-val-low").html(getValidValue(zillow.zestimate.valuation_low));
    $(".table-val-high").html(getValidValue(zillow.zestimate.valuation_high));
    $(".table-percen").html(getValidValue(zillow.zestimate.percentile));
     
    ///id for rent zestimate
    $("#table-zestimate").html(getValidValue(zillow.rent_zestimate.zestimate));
    $("#table-updated").html(getValidValue(zillow.rent_zestimate.last_updated));
    $("#table-val-change").html(getValidValue(zillow.rent_zestimate.value_change));
    $("#table-val-low").html(getValidValue(zillow.rent_zestimate.valuation_low));
    $("#table-val-high").html(getValidValue(zillow.rent_zestimate.valuation_high));
    $("#table-percen").html(getValidValue(zillow.rent_zestimate.percentile));
     






}



$(document).ready(function (event) {

   $('#z-previous').click(function(){
      Zillow.setIndex(-1);
      updateZillowView();

   });


  $('#z-next').click(function(){
     
           Zillow.setIndex(1);
           updateZillowView();
   });


    $("#search-form").submit(function (event) {

        event.preventDefault();
        $('.fa-spin').css("display","inline");       
        $('.fa-check').css("display","none");
        $('.fa-close').css("display","none");
 
        $.ajax({
            url: $(this).attr("js-search-url"),
            type: $(this).attr("method"),
            data: $(this).serialize(),
            dataType: 'json',
            success: function (data) {
                $('.fa-spin').css("display","none");
                $('.fa-check').css("display","inline");
                
                Zillow.set(JSON.parse(data));
                $('#z-total').html(Zillow.datas().length);
                updateZillowView();
            },


            error: function (request, status, error) {
                 $('.fa-spin').css("display","none");
                 $('.fa-close').css("display","inline");
                 
                
            }
        });


    });
});
