from modeltranslation.translator import translator, TranslationOptions
from django.contrib.flatpages.models import FlatPage
from .models import (
    Room,
    ProgramCategory, ProgramTime,
    Sponsor, SponsorLevel,
    Speaker, Program,
    Announcement, Jobfair
)


class FlatPageTranslationOptions(TranslationOptions):
    fields = ('title', 'content',)
translator.register(FlatPage, FlatPageTranslationOptions)


class RoomTranslationOptions(TranslationOptions):
    fields = ('name', 'desc',)
translator.register(Room, RoomTranslationOptions)


class ProgramCategoryTranslationOptions(TranslationOptions):
    fields = ('name',)
translator.register(ProgramCategory, ProgramCategoryTranslationOptions)


class ProgramTimeTranslationOptions(TranslationOptions):
    fields = ('name',)
translator.register(ProgramTime, ProgramTimeTranslationOptions)


class SponsorTranslationOptions(TranslationOptions):
    fields = ('name', 'desc',)
translator.register(Sponsor, SponsorTranslationOptions)


class SponsorLevelTranslationOptions(TranslationOptions):
    fields = ('name', 'desc',)
translator.register(SponsorLevel, SponsorLevelTranslationOptions)


class SpeakerTranslationOptions(TranslationOptions):
    fields = ('name', 'desc',)
translator.register(Speaker, SpeakerTranslationOptions)


class ProgramTranslationOptions(TranslationOptions):
    fields = ('name', 'desc',)
translator.register(Program, ProgramTranslationOptions)


class AnnouncementTranslationOptions(TranslationOptions):
    fields = ('title', 'desc',)
translator.register(Announcement, AnnouncementTranslationOptions)


class JobfairTranslationOptions(TranslationOptions):
    fields = ('name', 'desc',)
translator.register(Jobfair, JobfairTranslationOptions)
