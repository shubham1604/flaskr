from flask_admin.contrib.sqla import ModelView


class PostModelView(ModelView):
    can_create = True
    can_delete = True
    can_edit = True
    create_modal = True
    edit_modal = True
    column_filters = ["title", "body"]
    column_searchable_list = ["body", "body", ]
    can_view_details = True
    can_export = True

    form_widget_args = {
        "id": {"readonly": True},
        "created": {"readonly": True, "disabled": True},
    }


class UserModelView(ModelView):
    can_create = False
    can_delete = False
    can_edit = False
    column_exclude_list = ["password"]
