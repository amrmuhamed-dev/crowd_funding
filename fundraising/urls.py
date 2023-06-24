from django.urls import path
from fundraising.views import *
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [

    path('search',Search,name='search'),
    path('create_campaign',create_campaign,name='create_campaign'),
    path('update_campaign/<int:compaign_id>',Update_campaign,name='update_campaign'),
    path('delete_campaign/<int:compaign_id>',Delete_campaign,name='delete_campaign'),
    path('all_compaign',All_compaign,name='all_compaign'),
    path('add_comment/<int:compaign_id>',Add_comment,name='add_comment'),
    path('reply_comment/',Reply_comment,name='reply_comment'),
    path('report_compaign/<int:compaign_id>',Report_compaign,name='report_compaign'),
    path('report_comment/<int:comment_id>',Report_comment,name='report_comment'),
    path('donate_compaign/<int:compaign_id>',Donate_compaign,name='donate_compaign')

# 
    
 
]+static(settings.MEDIA_DIR, document_root=settings.MEDIA_ROOT)