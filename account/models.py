from django.db import models
from django.utils import timezone
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.urls import reverse


class Brand(models.Model):
    CATEGORY = (
        ('aml', 'aml'), ('analytics', 'analytics'), ('app', 'app'), ('assetmanagement', 'assetmanagement'),
        ('authentication', 'authentication'), ('blockchainexplorer', 'blockchainexplorer'),
        ('Blockchains', 'Blockchains'), ('blog', 'blog'), ('card', 'card'), ('community', 'community'),
        ('conference', 'conference'), ('consulting', 'consulting'), ('cryptobanking', 'cryptobanking'),
        ('cryptobrokerage', 'cryptobrokerage'),
        ('cryptoconglomerate', 'cryptoconglomerate'), ('cryptofinance', 'cryptofinance'),
        ('cryptofundofunds', 'cryptofundofunds'), ('cryptohedgefund', 'cryptohedgefund'), ('custody', 'custody'),
        ('dapp', 'dapp'), ('defi', 'defi'), ('derivatives', 'derivatives'), ('dex', 'dex'),
        ('ecommercetools', 'ecommercetools'), ('education', 'education'), ('exchange', 'exchange'),
        ('fintech', 'fintech'), ('gaming', 'gaming'), ('hardwarewallet', 'hardwarewallet'),
        ('informationhub', 'informationhub'), ('infrastructure', 'infrastructure'),
        ('investmentplatform', 'investmentplatform'), ('jobsincrypto', 'jobsincrypto'), ('kyc', 'kyc'),
        ('legal', 'legal'), ('lending', 'lending'), ('marketdata', 'marketdata'),
        ('marketingagency', 'marketingagency'),
        ('marketmaking', 'marketmaking'), ('marketplace', 'marketplace'), ('masternodes', 'masternodes'),
        ('medianetwork', 'medianetwork'), ('mining', 'mining'), ('newsletter', 'newsletter'),
        ('newsoutlet', 'newsoutlet'), ('nft', 'nft'), ('otc', 'otc'), ('payments', 'payments'), ('podcast', 'podcast'),
        ('portfoliotracker', 'portfoliotracker'), ('prfirm', 'prfirm'), ('protocol', 'protocol'),
        ('quantitativetrading', 'quantitativetrading'), ('research', 'research'), ('saas', 'saas'), ('shop', 'shop'),
        ('socialtrading', 'socialtrading'), ('staking', 'staking'), ('thinktank', 'thinktank'),
        ('tokensaleplatform', 'tokensaleplatform'), ('tokensolutions', 'tokensolutions'), ('tool', 'tool'),
        ('trading', 'trading'), ('tradingdesk', 'tradingdesk'), ('tradinggroup', 'tradinggroup'),
        ('venturecapital', 'venturecapital'), ('wallet', 'wallet'), ('wallet', 'wallet'),
    )
    title = models.CharField(max_length=100)
    website = models.URLField(blank=False)
    language = models.CharField(max_length=220, null=True)
    category = models.CharField(max_length=200, null=True, choices=CATEGORY)
    created = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, null=True, blank=True)

    def __str__(self):
        return str(self.title)

    # def get_absolute_url(self):
    #     return reverse('', kwargs={'slug': self.slug})


def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Brand.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug


def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)


pre_save.connect(pre_save_post_receiver, sender=Brand)


class Content(models.Model):
    title = models.ForeignKey(Brand, on_delete=models.CASCADE)
    month_name = models.CharField(max_length=220)
    monthly_active_user = models.PositiveIntegerField()
    global_rank = models.PositiveIntegerField()
    country_traffic = models.CharField(max_length=220)
    social_media_traffic = models.PositiveIntegerField()
    updated = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'"Brand: {self.title}" - "Month: {self.month_name}"'
