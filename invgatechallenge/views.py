# -*- coding: utf-8 -*-

import random
from hashlib import sha256

from django.shortcuts import render
from django import forms
from captcha.fields import CaptchaField
from django.conf import settings

from invgatechallenge.models import Submission, Token, HackDetection


def generate_digest(number_one, number_two, number_three, token=None):
    if token is None:
        t = Token()
        t.save()
        token = t.pk
    sha = sha256()
    sha.update(settings.SECRET_PREFIX)
    sha.update(str(number_one) + "_" + str(number_two) + "_" + str(number_three) + "_" + str(token))
    sha.update(settings.SECRET_SUFFIX)
    digest = str(token) + "_" + sha.hexdigest()
    return digest


def mark_token_as_used(token_id):
    Token.objects.filter(id=token_id).delete()


class ChallengeForm(forms.Form):
    email = forms.EmailField()
    number_one = forms.IntegerField(widget=forms.HiddenInput())
    solution_one = forms.IntegerField(label='Respuesta Desafío 1)')
    number_two = forms.IntegerField(widget=forms.HiddenInput())
    solution_two = forms.IntegerField(label='Respuesta Desafío 2)')
    number_three = forms.IntegerField(widget=forms.HiddenInput())
    solution_three = forms.IntegerField(label='Respuesta Desafío 3)')
    anti_tampering = forms.CharField(widget=forms.HiddenInput())

    captcha = CaptchaField()

    def clean(self):
        cleaned_data = super(ChallengeForm, self).clean()
        old_digest = cleaned_data.get("anti_tampering", '')
        index = old_digest.find("_")
        token_id = old_digest[0:index]
        digest = generate_digest(cleaned_data.get('number_one', ''), cleaned_data.get('number_two', ''),
                                 cleaned_data.get('number_three', ''), token_id)
        try:
            token = Token.objects.get(id=token_id)
        except Token.DoesNotExist as e:
            token = None

        if index == -1 or digest != cleaned_data.get("anti_tampering", '') or token is None:
            self.add_error(None,
                           'Parece que nos queres hackear. Si seguis tratando lo vas a poder hacer, pero no es la idea. Dale! Copate!')
            HackDetection(email = cleaned_data.get('email', '')).save()
        mail = cleaned_data.get('email', '')
        if '+' in mail:
            self.add_error('email', 'El caracter + no esta permitido')
        self.cleaned_data["anti_tampering"] = generate_digest(cleaned_data.get('number_one', ''),
                                                              cleaned_data.get('number_two', ''),
                                                              cleaned_data.get('number_three', ''))
        self.data = self.cleaned_data
        mark_token_as_used(token_id)
        return cleaned_data


data = {1: 10, 2: 20, 3: 46, 4: 104, 5: 240, 6: 544, 7: 1256, 8: 2848, 9: 6576, 10: 14912, 11: 34432, 12: 78080,
        13: 180288, 14: 408832, 15: 944000, 16: 2140672, 17: 4942848, 18: 11208704, 19: 25881088, 20: 58689536,
        21: 135515136, 22: 307302400, 23: 709566464, 24: 1609056256, 25: 3715338240L, 26: 8425127936L, 27: 19453763584L,
        28: 44114542592L, 29: 101861228544L, 30: 230986743808L, 31: 533352316928L, 32: 1209462292480L,
        33: 2792668987392L, 34: 6332826779648L, 35: 14622604656640L, 36: 33159111507968L, 37: 76564951990272L,
        38: 173623361929216L, 39: 400899293315072L, 40: 909103725543424L, 41: 2099135951929344L, 42: 4760128905543680L,
        43: 10991218538315776L, 44: 24924358531088384L, 45: 57550767422177280L, 46: 130505635564355584L,
        47: 301339730379800576L, 48: 683336379261779968L, 49: 1577835312590094336L, 50: 3577995733313257472L,
        51: 8261652954021363712L, 52: 18734628882832424960L, 53: 43258576473767804928L, 54: 98095790363741519872L,
        55: 226504847026521374720L, 56: 513636226651119419392L, 57: 1185994776264057028608L,
        58: 2689434198451750436864L, 59: 6209949269478256672768L, 60: 14082060284106024943616L,
        61: 32515716511813311922176L, 62: 73734624910829147914240L, 63: 170254501992966844841984L,
        64: 386079508328550787710976L, 65: 891464145910547821363200L, 66: 2021538550327988134608896L,
        67: 4667766867491419548811264L, 68: 10584913268653725656809472L, 69: 24440744621306326007414784L,
        70: 55423325410610401402421248L, 71: 127973400257872277849243648L, 72: 290200299389047505787289600L,
        73: 670077423062008363065802752L, 74: 1519508494691843429114052608L, 75: 3508570937340561066997841920L,
        76: 7956249770594870551535157248L, 77: 18371115931795332949723840512L, 78: 41659464644801849592754733056L,
        79: 96192411841409753430351675392L, 80: 218131788786431615350387769344L, 81: 503670007321277188783214690304L,
        82: 1142152874139382293731307683840L, 83: 2637250396562024118977881440256L,
        84: 5980390089690567300986295025664L, 85: 13808822350087035958734429880320L,
        86: 31313729041585874630992539418624L, 87: 72303932514274119276495053520896L,
        88: 163960813890752978582010056409088L, 89: 378588305685296571824032601604096L,
        90: 858509967178174372968090180780032L, 91: 1982314104054682953838215395540992L,
        92: 4495216547506034323480500859043840L, 93: 10379531401586911435733161966829568L,
        94: 23537259416323508449010644431142912L, 95: 54347931993302736799046110218813440L,
        96: 123242690307916913400141863150682112L, 97: 284569466353468775051344013445562368L,
        98: 645307104182207446604808601179521024L, 99: 1490025070147601703111879639798120448L}


def validate_solution(n, res):
    real_res = data.get(n, None)
    return (not (real_res is None)) and res == real_res


def choice_numbers():
    candidates_one = random.choice(range(3, 15))
    candidates_two = random.choice(range(15, 50))
    candidates_three = random.choice(range(50, 100))
    return (candidates_one, candidates_two, candidates_three )


def generate_form(candidates_one, candidates_two, candidates_three):
    digest = generate_digest(candidates_one, candidates_two, candidates_three, None)
    form = ChallengeForm({'number_one': candidates_one, 'number_two': candidates_two, 'number_three': candidates_three,
                          'anti_tampering': digest})
    return form


# Create your views here.
def present_challenge(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ChallengeForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            if Submission.objects.filter(email=form.cleaned_data.get('email'), is_correct=True).exists():
                return render(request, 'already_submitted.html')
            failed = False
            for n, res in [(form.cleaned_data.get('number_one'), form.cleaned_data.get('solution_one')),
                           (form.cleaned_data.get('number_two'), form.cleaned_data.get('solution_two')),
                           (form.cleaned_data.get('number_three'), form.cleaned_data.get('solution_three'))]:
                if not validate_solution(n, res):
                    failed = True
                    break

            s = Submission(email=form.cleaned_data.get('email'), is_correct=not failed)
            s.save()
            if failed:
                # candidates_one, candidates_two, candidates_three =  choice_numbers()
                # form = generate_form(candidates_one, candidates_two, candidates_three)
                candidates_one, candidates_two, candidates_three = map(lambda x: form.cleaned_data.get(x),
                                                                       ['number_one', 'number_two', 'number_three'])
                return render(request, 'failed.html', {'form': form, 'first': candidates_one, 'second': candidates_two,
                                                       'third': candidates_three})
            else:
                return render(request, 'thanks.html')
        else:
            # candidates_one, candidates_two, candidates_three =  choice_numbers()
            # form = generate_form(candidates_one, candidates_two, candidates_three)
            candidates_one, candidates_two, candidates_three = map(lambda x: form.cleaned_data.get(x),
                                                                   ['number_one', 'number_two', 'number_three'])
            return render(request, 'challenge.html',
                          {'form': form, 'first': candidates_one, 'second': candidates_two, 'third': candidates_three})

    # if a GET (or any other method) we'll create a blank form
    else:
        candidates_one, candidates_two, candidates_three = choice_numbers()
        form = generate_form(candidates_one, candidates_two, candidates_three)
        return render(request, 'challenge.html',
                      {'form': form, 'first': candidates_one, 'second': candidates_two, 'third': candidates_three})
