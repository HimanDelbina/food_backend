from django.db import models
from django_jalali.db import models as jmodels


class UnitModel(models.Model):
    name = models.CharField(verbose_name="واحد", max_length=50)

    class Meta:
        verbose_name = "واحد"
        verbose_name_plural = "واحد"

    def __str__(self):
        return self.name


class PostWorkModel(models.Model):
    name = models.CharField(verbose_name="پست شغلی", max_length=50)

    class Meta:
        verbose_name = "پست شغلی"
        verbose_name_plural = "پست شغلی"

    def __str__(self):
        return self.name


class WorkTypeModel(models.Model):
    name = models.CharField(verbose_name="عنوان شغلی", max_length=50)

    class Meta:
        verbose_name = "عنوان شغلی"
        verbose_name_plural = "عنوان شغلی"

    def __str__(self):
        return self.name


class OstanModel(models.Model):
    name = models.CharField(verbose_name="استان", max_length=50)

    class Meta:
        verbose_name = "استان"
        verbose_name_plural = "استان"

    def __str__(self):
        return self.name


class CityModel(models.Model):
    ostan = models.ForeignKey(
        OstanModel, verbose_name="استان", on_delete=models.CASCADE
    )
    name = models.CharField(verbose_name="شهرستان", max_length=50)

    class Meta:
        verbose_name = "شهرستان"
        verbose_name_plural = "شهرستان"

    def __str__(self):
        return self.name


CHILDGENDER = (("M", "پسر"), ("W", "دختر"))


class ChildModel(models.Model):
    name = models.CharField(verbose_name="نام", max_length=50)
    gender = models.CharField(
        choices=CHILDGENDER, verbose_name="نوع فرزند", max_length=2
    )
    birthday = jmodels.jDateTimeField(
        verbose_name="تاریخ تولد",
        auto_now=False,
        auto_now_add=False,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "فرزند"
        verbose_name_plural = "فرزند"

    def __str__(self):
        return self.name


SHIFT_WORK = (
    ("R", "روزکار"),
    ("SH", "عصر و شب"),
)
ISONLINE = (
    ("A", "فعال"),
    ("MA", "مامور"),
    ("MO", "مشاور"),
)
GENDER = (("M", "مرد"), ("W", "زن"))

SOLDER_SELECT = (("P", "پایان خدمت"), ("M", "معافیت"))
EDUCATION_SELECT = (
    ("DE", "ابتدایی"),
    ("DR", "راهنمایی"),
    ("DS", "سیکل"),
    ("DD", "دبیرستان"),
    ("DI", "دیپلم"),
    ("FD", "کاردانی"),
    ("LI", "کارشناسی"),
    ("FL", "کارشناسی ارشد"),
    ("PD", "دکترا"),
    ("DA", "دانشجو"),
)
ACCESS_SELECT = (
    ("US", "کارمند"),
    ("KA", "کارگزینی"),
    ("HE", "حسابداری"),
    ("AN", "انبار"),
    ("MO", "مدیریت"),
    ("NE", "نگهبانی"),
    ("BA", "بازرگانی"),
)


class PersonelModel(models.Model):
    person_code = models.CharField(verbose_name="شماره پرسنلی", max_length=10)
    password = models.CharField(verbose_name="رمز عبور", max_length=50)
    first_name = models.CharField(verbose_name="نام", max_length=50)
    last_name = models.CharField(verbose_name="نام خانوادگی", max_length=50)
    date_employ = jmodels.jDateField(
        verbose_name="تاریخ استخدام ",
        auto_now=False,
        auto_now_add=False,
        null=True,
        blank=True,
    )
    unit = models.ForeignKey(UnitModel, verbose_name="واحد", on_delete=models.CASCADE)
    work_type = models.ForeignKey(
        WorkTypeModel, verbose_name="عنوان شغلی", on_delete=models.CASCADE
    )
    post_work = models.ForeignKey(
        PostWorkModel, verbose_name="پست شغلی", on_delete=models.CASCADE
    )
    shift = models.CharField(choices=SHIFT_WORK, verbose_name="شیفت", max_length=2)
    is_online = models.CharField(
        choices=ISONLINE, verbose_name="نحوه کار با شرکت", max_length=2
    )
    is_active = models.BooleanField(default=True, verbose_name="آیا فعال است ؟")
    phone_number = models.CharField(verbose_name="شماره موبایل", max_length=11)
    melli_code = models.CharField(verbose_name="کد ملی", max_length=10)
    sh_code = models.CharField(
        verbose_name="شماره شناسنامه", max_length=10, null=True, blank=True
    )
    sh_s_code = models.CharField(
        verbose_name="شماره سریال شناسنامه", max_length=15, null=True, blank=True
    )
    father_name = models.CharField(verbose_name="نام پدر", max_length=50)
    birthday = jmodels.jDateField(
        verbose_name="تاریخ تولد ",
        auto_now=False,
        auto_now_add=False,
        null=True,
        blank=True,
    )
    sh_ostan = models.ForeignKey(
        OstanModel,
        verbose_name="استان محل تولد",
        on_delete=models.CASCADE,
        related_name="sh_ostan",
    )
    burn_ostan = models.ForeignKey(
        CityModel,
        verbose_name="محل صدور",
        on_delete=models.CASCADE,
        related_name="burn_ostan",
    )
    gender = models.CharField(choices=GENDER, verbose_name="جنسیت", max_length=2)
    solder_select = models.CharField(
        choices=SOLDER_SELECT,
        verbose_name="وضعیت نظام وظیفه",
        max_length=2,
        null=True,
        blank=True,
    )
    reason_ex = models.CharField(
        verbose_name="دلیل معافیت", max_length=50, null=True, blank=True
    )
    education = models.CharField(
        choices=EDUCATION_SELECT, verbose_name="آخرین مدرک تحصیلی", max_length=50
    )
    education_field = models.CharField(
        verbose_name="رشته تحصیلی", max_length=50, null=True, blank=True
    )
    univercity = models.CharField(
        verbose_name="دانشگاه", max_length=50, null=True, blank=True
    )
    Institute = models.CharField(
        verbose_name="موسسه", max_length=50, null=True, blank=True
    )
    ev_file = models.BooleanField(
        default=False, verbose_name="مدرک در پرونده", null=True, blank=True
    )
    is_marid = models.BooleanField(default=True, verbose_name="وضعیت تاهل")
    wife_name = models.CharField(
        verbose_name="نام همسر", max_length=50, null=True, blank=True
    )
    wife_birthday = jmodels.jDateField(
        verbose_name="تاریخ تولد همسر",
        auto_now=False,
        auto_now_add=False,
        null=True,
        blank=True,
    )
    child_count = models.IntegerField(
        verbose_name="تعداد فرزند", default=0, null=True, blank=True
    )
    boy_child_count = models.IntegerField(
        verbose_name="تعداد فرزند پسر", default=0, null=True, blank=True
    )
    girl_child_count = models.IntegerField(
        verbose_name="تعداد فرزند دختر", default=0, null=True, blank=True
    )
    child = models.ManyToManyField(
        ChildModel, verbose_name="فرزند", null=True, blank=True
    )
    insurance_number = models.CharField(
        verbose_name="شماره بیمه", max_length=15, null=True, blank=True
    )
    insurance_history_day = models.CharField(
        verbose_name="سابقه بیمه قبل استخدام(روز)", max_length=15, null=True, blank=True
    )
    insurance_history_year = models.CharField(
        verbose_name="سابقه بیمه قبل استخدام(سال)", max_length=15, null=True, blank=True
    )
    bank_number = models.CharField(
        verbose_name="شماره حساب", max_length=20, null=True, blank=True
    )
    bank_shaba = models.CharField(
        verbose_name="شماره شبا", max_length=30, null=True, blank=True
    )
    address = models.TextField(verbose_name="آدرس", null=True, blank=True)
    post_code = models.CharField(
        verbose_name="کد پستی", max_length=50, null=True, blank=True
    )
    settlement_date = jmodels.jDateField(
        verbose_name="تاریخ تسویه",
        auto_now=False,
        auto_now_add=False,
        null=True,
        blank=True,
    )
    settlement_description = models.TextField(
        verbose_name="دلیل تسویه",
        null=True,
        blank=True,
    )

    settlement_steps = models.BooleanField(verbose_name="در حال تصفیه", default=False)
    issue_date = jmodels.jDateField(
        verbose_name="تاریخ صدور",
        auto_now=False,
        auto_now_add=False,
        null=True,
        blank=True,
    )
    married_date = jmodels.jDateField(
        verbose_name="تاریخ عقد",
        auto_now=False,
        auto_now_add=False,
        null=True,
        blank=True,
    )
    access = models.CharField(
        verbose_name="سطح دسترسی", choices=ACCESS_SELECT, max_length=3, default="US"
    )

    create_at = jmodels.jDateTimeField(auto_now_add=True)
    update_at = jmodels.jDateTimeField(auto_now=True)

    class Meta:
        verbose_name = "پرسنل"
        verbose_name_plural = "پرسنل"

    def __str__(self):
        return str(self.person_code)
