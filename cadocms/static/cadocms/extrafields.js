if (jQuery != undefined) {
    var django = {
        'jQuery':jQuery
    }
}
(function($){
    $(document).ready(function($) {
    	
    	function saveExtra(extraDiv){
    		//console.log('save');
			var extra = {};
			extraDiv.find("[name^=extra]").each(function(i, elem){
				if($(elem).attr('name') != 'extra')
				{
					var ekey = $(elem).attr('name').substring(6, $(elem).attr('name').length-1);
					if ($(elem).attr('type') == 'checkbox')
					{
						extra[ekey] = $(elem).is(":checked");
					}
					else
					{
						extra[ekey] = $(elem).val();
					}
				}
			});
			//console.log(extra);
			extraDiv.parent().find('textarea').first().val(JSON.stringify(extra));
		}
		
		function loadExtra(extraDiv){
			var extra = JSON.parse(extraDiv.parent().find('textarea').first().val());
			//console.log(extra);
			for (key in extra)
			{
				//console.log(extra[key])
				var elem = extraDiv.find("[name=extra\\[" + key + "\\]]");
				if (elem.is(':checkbox'))
				{
					elem.attr('checked', extra[key] ? 'checked' : false);
				}
				else
				{
					elem.val(extra[key]);
				}
			}
		}
		
		document.TemplateExtraAppended = false;
		
    	document.registerExtraField = function(url, field_name, provider_name)
    	{
    	   	//console.log(url, field_name, provider_name);
    		///cado/extrafields/unravelling.Item/4
    		//productoption_set-0-extra
    		var field;
    		if (field_name.indexOf('__prefix__') > 0) {
    			if(document.TemplateExtraAppended) {
    				s_start = 'id_' + field_name.substring(0, field_name.indexOf('__prefix__'));
    				s_end = field_name.substring(field_name.indexOf('__prefix__')+10);
    				//alert(s_start);alert(s_end);alert($('#' + s_start + '*' + s_end).length)
    				field = $('[id^="' + s_start + '"][id$="' + s_end + '"]').not(':last').last();
    				//alert(field.attr('id'));
    	    		//id_productoption_set-1-extra
    	    		
    			} else {
    				document.TemplateExtraAppended = true;
    				return 0;
    			}
    		} else {
    			field = $('#id_' + field_name);
    		}
			var extraDiv = $('<div class="extraFieldsDiv"></div>');
			//field.parents('.form-row').parent().children().first().hide();
			field.after(extraDiv);
			field.hide();
			//TODO grp-error
			var errorLists = {};
			if (field.parent().hasClass('error')) {
				//TODO
				field.parent().find('.errorlist li').each(function(i,e){
					var elist = $(e).text().split(':');
					var ekey = elist.shift()
					var etext = elist.join('|')
					if (!(ekey in errorLists)) {
						errorLists[ekey] = new Array();
					}
					errorLists[ekey].push(etext);
				});
				field.parent().find('.errorlist').hide();
				field.parent().removeClass('error');
			}
			if (provider_name.indexOf('.') > 0) {
				provider_name = provider_name.substring(0, provider_name.indexOf('.'));
			}
    		provider = $('#id_' + provider_name);

			provider.change(function(){
				$.get(url.replace('0', $(this).val()), {}, function(data){
					extraDiv.html(data);
					
					for (var k in errorLists){
						var $elem = extraDiv.find('[name=\'extra\[' + k + '\]\']');
						$elem.parent().addClass('error');
						var $ul = $('<ul class="errorlist"></ul>');
						for (error in errorLists[k]){
							$ul.append($('<li></li>').text(errorLists[k][error]));
						}
						$elem.parent().prepend($ul);
					}
					errorLists = {};
					
					extraDiv.find("[name^=extra]").change(function(){
						saveExtra(extraDiv);
					});
					loadExtra(extraDiv);
					extraDiv.find(".extraMyDateField").datepicker({
			        	format:'dd/mm/yyyy',
			        	autoclose: true
					});
					extraDiv.find(".extraMyTimeField").wrap('<span class="bootstrap-timepicker"/>');
					
					extraDiv.find(".extraMyTimeField").after('<i class="icon-time" style="margin: -2px 0 0 -22.5px; pointer-events: none; position: relative;"></i>');
					extraDiv.find(".extraMyTimeField").timepicker({
		                minuteStep: 5,
		                showInputs: false,
		                defaultTime: false
		                //disableFocus: true
		            });
				}, 'html');
			});
			
			provider.change();
    	}
    	
    	document.registerExtraFieldsQueue = function() {
            if (typeof document.extraFieldsQueue !== 'undefined')
            {
                while ((extraParams = document.extraFieldsQueue.pop()) != null)
                {
                    document.registerExtraField(extraParams[0], extraParams[1], extraParams[2]);
                }
            }
        }
        document.registerExtraFieldsQueue();
    });
})(django.jQuery);