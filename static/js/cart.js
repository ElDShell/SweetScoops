$(document).ready(function(){
    $(".increase-btn").click(function(){
        var itemId =$(this).data('cart-item-id');
        $.ajax({
            url:'/carts/cart/item/update/',
            method:'post',
            data:{
                'item_id':itemId,
                'action':'increase',
                'csrfmiddlewaretoken':$('input[name="csrfmiddlewaretoken"]').val()
            },
            success: function(response){
                if (response.success){
                    $('#item-'+itemId+'-quantity').text(response.new_quantity);
                    $('#item-'+itemId+'-price').text('$'+response.new_price);
                    $('.cart-price').text('Total:$'+response.new_total_price);
                }

            }
        });
    });
    $('.decrease-btn').click(function(){
        var itemId = $(this).data('cart-item-id');
        $.ajax({
            url:'/carts/cart/item/update/',
            method:'post',
            data:{
                'item_id':itemId,
                'action':'decrease',
                'csrfmiddlewaretoken':$('input[name="csrfmiddlewaretoken"]').val()
            },
            success: function(response){
                if (response.success){
                    $('#item-' + itemId +'-quantity').text(response.new_quantity);
                    $('#item-'+itemId+'-price').text('$'+response.new_price);
                    $('.cart-price').text('Total:$'+response.new_total_price);
                }
            },
            error: function(xhr,errmsg,err){
                alert("Error"+errmsg)
            }
        });
    });
});