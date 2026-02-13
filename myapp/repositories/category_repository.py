from ..entity import Category


class CategoryRepository:
    def list_by_user(self, user_id: str):
        return Category.objects.select_related("parent").filter(user_id=user_id)

    def list_all(self):
        return Category.objects.select_related("parent").all()

    def get_by_id_user(self, pk: int, user_id: str):
        return (
            Category.objects.select_related("parent")
            .filter(pk=pk, user_id=user_id)
            .first()
        )

    def get_by_id(self, pk: int):
        return Category.objects.select_related("parent").filter(pk=pk).first()

    def exists_by_name_user(self, name: str, user_id: str, exclude_id: int | None = None):
        qs = Category.objects.filter(name=name, user_id=user_id)
        if exclude_id is not None:
            qs = qs.exclude(pk=exclude_id)
        return qs.exists()

    def get_parent(self, parent_id: int, user_id: str | None):
        return Category.objects.filter(pk=parent_id, user_id=user_id).first()

    def create(self, **fields):
        return Category.objects.create(**fields)

    def save(self, instance: Category):
        instance.save()
        return instance

    def delete(self, instance: Category):
        instance.delete()
