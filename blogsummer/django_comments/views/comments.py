from __future__ import absolute_import

from django import http
from django.apps import apps
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import models
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.html import escape
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST

import django_comments
from django_comments import signals
from django_comments.views.utils import next_redirect, confirmation_view

#添加这两个引用，为了返回json数据
from django.http import JsonResponse


class CommentPostBadRequest(http.HttpResponseBadRequest):
    """
    Response returned when a comment post is invalid. If ``DEBUG`` is on a
    nice-ish error message will be displayed (for debugging purposes), but in
    production mode a simple opaque 400 page will be displayed.
    """

    def __init__(self, why):
        super(CommentPostBadRequest, self).__init__()
        if settings.DEBUG:
            self.content = render_to_string("comments/400-debug.html", {"why": why})


@csrf_protect
@require_POST



def post_comment(request, next=None, using=None):
    """
    Post a comment.

    HTTP POST is required. If ``POST['submit'] == "preview"`` or if there are
    errors a preview template, ``comments/preview.html``, will be rendered.
    """
    # Fill out some initial data fields from an authenticated user, if present
    data = request.POST.copy()
    # if request.user.is_authenticated():
    #     if not data.get('name', ''):
    #         data["name"] = request.user.get_full_name() or request.user.get_username()
    #     if not data.get('email', ''):
    #         data["email"] = request.user.email
    #     #changes
    #     return JsonResponse({"result_info":"未认证用户"})

    # Look up the object we're trying to comment about
    ctype = data.get("content_type")
    object_pk = data.get("object_pk")
    if ctype is None or object_pk is None:
        #return CommentPostBadRequest("Missing content_type or object_pk field.")
        return JsonResponse({"result_info":"Missing content_type or object_pk field"})
    try:
        model = apps.get_model(*ctype.split(".", 1))
        target = model._default_manager.using(using).get(pk=object_pk)
    except TypeError:
        #return CommentPostBadRequest(
          #  "Invalid content_type value: %r" % escape(ctype))
        return JsonResponse({"result_info":"Invalid content_type value"})
    except AttributeError:
        # return CommentPostBadRequest(
        #     "The given content-type %r does not resolve to a valid model." % escape(ctype))
        return JsonResponse({"result_info":"The given content-type does not resolve to a valid model"})
    except ObjectDoesNotExist:
        # return CommentPostBadRequest(
        #     "No object matching content-type %r and object PK %r exists." % (
        #         escape(ctype), escape(object_pk)))
        return JsonResponse({"result_info":"No object matching content-type and object PK exists"})
    except (ValueError, ValidationError) as e:
        # return CommentPostBadRequest(
        #     "Attempting go get content-type %r and object PK %r exists raised %s" % (
        #         escape(ctype), escape(object_pk), e.__class__.__name__))
        return JsonResponse({"result_info":"Attempting go get content-type and object PK  exists raised"})
    # Do we want to preview the comment?
    preview = "preview" in data

    # Construct the comment form
    form = django_comments.get_form()(target, data=data)

    # Check security information
    if form.security_errors():
        # return CommentPostBadRequest(
        #     "The comment form failed security verification: %s" % escape(str(form.security_errors())))
        return JsonResponse({"result_info":"The comment form failed security verification"})
    # If there are errors or if we requested a preview show the comment
    if form.errors or preview:
        template_list = [
            # These first two exist for purely historical reasons.
            # Django v1.0 and v1.1 allowed the underscore format for
            # preview templates, so we have to preserve that format.
            "comments/%s_%s_preview.html" % (model._meta.app_label, model._meta.model_name),
            "comments/%s_preview.html" % model._meta.app_label,
            # Now the usual directory based template hierarchy.
            "comments/%s/%s/preview.html" % (model._meta.app_label, model._meta.model_name),
            "comments/%s/preview.html" % model._meta.app_label,
            "comments/preview.html",
        ]
        # return render(request, template_list, {
        #         "comment": form.data.get("comment", ""),
        #         "form": form,
        #         "next": data.get("next", next),
        #     }
        # )
        return JsonResponse({"result_info":"form.error or preview"})

    # Otherwise create the comment
    comment = form.get_comment_object()
    comment.ip_address = request.META.get("REMOTE_ADDR", None)
       #change 2016-05-12
    comment.root_id = data.get('root_id',0)
    comment.reply_to = data.get('reply_to',0)
    comment.reply_name = data.get('reply_name','')
    
    if request.user.is_authenticated():
        comment.user = request.user

    # Signal that the comment is about to be saved
    responses = signals.comment_will_be_posted.send(
        sender=comment.__class__,
        comment=comment,
        request=request
    )

    for (receiver, response) in responses:
        if response is False:
            # return CommentPostBadRequest(
            #     "comment_will_be_posted receiver %r killed the comment" % receiver.__name__)
            return JsonResponse({"result_info":"comment_will_be_posted receiver  killed the comment"})

    # Save the comment and signal that it was saved
    comment.save()
 
    signals.comment_was_posted.send(
        sender=comment.__class__,
        comment=comment,
        request=request
    )
 
    return_data={
        "user_name":comment.user_name ,
        "submit_date":comment.submit_date.strftime('%Y-%m-%d %H:%M'),
        "comment":comment.comment,
        "result_info":"success"
    }
    return JsonResponse( return_data)
    #return next_redirect(request, fallback=next or 'comments-comment-done', c=comment._get_pk_val())


comment_done = confirmation_view(
    template="comments/posted.html",
    doc="""Display a "comment was posted" success page."""
)