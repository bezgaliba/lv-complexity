from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from dotenv import load_dotenv
import os
import requests
import json
import re
import nltk
import joblib
import numpy as np
import xml.etree.ElementTree as ET
from nltk.tokenize import sent_tokenize, word_tokenize
from collections import OrderedDict

nltk.download('punkt')

requests.packages.urllib3.disable_warnings()

load_dotenv()

app = Flask(__name__)
CORS(app)

app.config['DEBUG'] = os.environ.get('FLASK_DEBUG')

directory = os.path.dirname(__file__)
model_path = os.path.join(directory, "../../best_model.pkl")
best_model = joblib.load(model_path)


class ComplexityEval:
    def __init__(self, text):
        self.text = text

    def clean(self):
        cleansed_words = re.sub(r'[^\w\s]', '', self.text).lower()
        #print("Teksts pēc normalizācijas: ",cleansed_words,"\n")
        return cleansed_words

    def tokenize(self):
        cleansed_words = self.clean()
        tokens = word_tokenize(cleansed_words)
        return tokens

    def tokenizeSent(self):
        cleansed_sent = sent_tokenize(self.text)
        return cleansed_sent

    def ASL(self):
        sentences = re.split('[.!?]', self.text)
        sentences = [sentence for sentence in sentences if sentence.strip()]
        words = self.tokenize()
        #print("Teksts pēc sadalīšana tekstvienībās: ",words,"\n\n")
        word_count = len(words)
        sentences_count = len(sentences)
        asl = word_count / sentences_count
        return round(asl, 2)
    
    def longWords(self):
        words_list = self.tokenize()
        count_long_words = 0
        for word in words_list:
            if len(word) > 6:
                count_long_words += 1        
        return count_long_words
    
    def GVD(self, longwordCount):
        word_count =  len(self.tokenize())
        metric_result = (longwordCount / word_count) * 100
        return round(metric_result, 2)

    def lvLasamibasMeginajums(self, longWords):
        metric_result = self.GVD(longWords) + self.ASL()
        return round(metric_result, 0)
    
    def lvLasamibas_grade(self, lvLasamibaKoeficients):
        grade_meaning = "Lasāmības pakāpe: "
        if lvLasamibaKoeficients > 54:
            grade_meaning += "Ļoti grūts"
        elif lvLasamibaKoeficients >= 45:
            grade_meaning += "Grūts"
        elif lvLasamibaKoeficients >= 35:
            grade_meaning += "Vidēji grūts"
        elif lvLasamibaKoeficients >= 25:
            grade_meaning += "Viegls"
        elif lvLasamibaKoeficients > 0 and lvLasamibaKoeficients < 24:
            grade_meaning += "Ļoti viegls"
        else:
            grade_meaning += "Nevar noteikt."

        return grade_meaning
    
    def replace_hyphens(self, data):
        return data.replace('<span class="hyphen">•</span>', '-')

    def syllableize(self, wordList):
        session = requests.Session()
        syllablesList = []
        response = session.get('https://www.ushuaia.pl/hyphen', verify=False)
        cookie = session.cookies.get_dict()
        for word in wordList:
            url = f"https://www.ushuaia.pl/hyphen/hyphenate.php?word={word}&lang=lv_LV"
            response = requests.get(url, cookies=cookie, verify=False)
            if response.status_code == 200:
                data = response.text
                cleanedData = self.replace_hyphens(data)
                syllablesList.append(cleanedData)
            else:
                print(f"Cookie auth error: {response.status_code}")
        return syllablesList

    def ASW(self, syllables):
        hyphen_counts = [syllable.count('-') + 1 for syllable in syllables]
        asw = sum(hyphen_counts) / len(hyphen_counts) if len(hyphen_counts) > 0 else 0
        return round(asw, 2)

    def flesch_reading_ease(self, asl, asw):
        metric_result = 206.835 - (1.015 * asl) - (84.6 * asw)
        return round(metric_result, 2)
    
    def flesch_reading_grade(self, flesch_reading_ease):
        grade_meaning = ""
        if flesch_reading_ease >= 90:
            grade_meaning = "Ļoti viegli lasāms. Vecuma līmenis: Pirmsskolas +"
        elif flesch_reading_ease >= 80:
            grade_meaning = "Viegli lasāms. Vecuma līmenis: 9 gadi +"
        elif flesch_reading_ease >= 70:
            grade_meaning = "Diezgan viegli lasāms. Vecuma līmenis: 10 gadi +"
        elif flesch_reading_ease >= 60:
            grade_meaning = "Vienkārši lasāms. Vecuma līmenis: 11 gadi +"
        elif flesch_reading_ease >= 50:
            grade_meaning = "Vidēji grūti lasāms. Vecuma līmenis: 13 gadi +"
        elif flesch_reading_ease >= 30:
            grade_meaning = "Grūti lasāms. Līmenis: koledžas, 18 gadi +"
        elif flesch_reading_ease >= 10:
            grade_meaning = "Ļoti grūti lasāms. Līmenis: koledžas absolvents, 21 gadi +"
        elif flesch_reading_ease >= 0:
            grade_meaning = "Ārkārtīgi grūti lasāms. Līmenis: profesionāla, 23 gadi +"
        else:
            grade_meaning = "Nevar noteikt."

        return grade_meaning
    
    def complex_words(self, syllables):
        words_to_remove = []
        for word in syllables:
            hyphen_count = word.count('-') + 1
            hyphen_count = hyphen_count
            if hyphen_count < 3:
                words_to_remove.append(word)

        for word_to_remove in words_to_remove:
            syllables.remove(word_to_remove)
        cleaned_complex_words = [syllable.replace('-', '') for syllable in syllables]
        return cleaned_complex_words

    def CWS(self, words, complex_words):
        cws = len(complex_words)/len(words)
        return cws

    def gunning_fog_index(self, asl, cws):
        metric_result = 0.4 * ((asl) + cws * 100)
        return round (metric_result, 2)

    def gunning_fog_grade(self, gunning_fog_grade):
        grade_meaning = "Līmenis: "
        if gunning_fog_grade >= 20:
            grade_meaning += "Universitātes"
        elif gunning_fog_grade >= 17:
            grade_meaning += "Vidusskolas absolventa"
        elif gunning_fog_grade >= 16:
            grade_meaning += "12. klases"
        elif gunning_fog_grade >= 13:
            grade_meaning += "10. - 11. klases"
        elif gunning_fog_grade >= 11:
            grade_meaning += "9. klases"
        elif gunning_fog_grade >= 10:
            grade_meaning += "8. klases"
        elif gunning_fog_grade >= 9:
            grade_meaning += "5. - 7. klases"
        elif gunning_fog_grade < 9:
            grade_meaning += "Sākumskolas un zem"
        else:
            grade_meaning += "Nevar noteikt."

        return grade_meaning

    def sentence_type(self, json_data):
        results = {}
        for key, value in json_data.items():
            sentences = value.get('sentences', [])
            text = value.get('text', '')

            sentence_results = []
            for sentence in sentences:
                tags = {'cs': False, 'cc': False, 'zc': False}
                for token in sentence.get('tokens', []):
                    if token['tag'] == 'cs':
                        tags['cs'] = True
                    if token['tag'] == 'cc':
                        tags['cc'] = True
                    if token['tag'] == 'zc':
                        tags['zc'] = True
                
                if tags['cs'] and tags['cc'] and tags['zc']:
                    sentence_results.append({'teikums': text, 'uzbuve': 'Salikts jaukts'})
                elif tags['cs'] and tags['zc'] and not tags['cc']:
                    sentence_results.append({'teikums': text, 'uzbuve': 'Salikts pakārtots'})
                elif tags['cc'] and tags['zc'] and not tags['cs']:
                    sentence_results.append({'teikums': text, 'uzbuve': 'Salikts sakārtots'})
                else:
                    sentence_results.append({'teikums': text, 'uzbuve': 'Vienkāršs'})
            
            results[key] = sentence_results
        return json.dumps(results, indent=2, ensure_ascii=False)

    def average_comma_count(self):
        sentences = self.text.split('.')
        sentencesCount = len(sentences)-1
        commaCount = 0
        for sentence in sentences:
            commaCount += sentence.count(',')
        if sentencesCount > 0:
            average = commaCount / sentencesCount
            return round(average, 2)
        else:
            return 0
    
    def NERRatio(self, analysisList, words):
        ner_count = {}
        total_words = len(words)
        total_ner = 0

        for teikums in analysisList.values():
            for sentence in teikums['sentences']:
                for ner_entity in sentence['ner']:
                    total_ner += 1
                    entity_text = ner_entity['text']
                    if entity_text in ner_count:
                        ner_count[entity_text] += 1
                    else:
                        ner_count[entity_text] = 1

        NERRatio = round(total_ner / total_words if total_words > 0 else 0, 2)

        NERList = {entity: count for entity, count in ner_count.items()}

        return NERRatio, json.dumps(NERList, indent=2, ensure_ascii=False)
    
    def getLemma(self, analysisList):
        lemmas = []
        symbolPattern = re.compile(r'[^\w\s]')

        for teikums_key, teikums_value in analysisList.items():
            sentences = teikums_value.get('sentences', [])
            for sentence in sentences:
                tokens = sentence.get('tokens', [])
                for token in tokens:
                    lemma = token.get('lemma')
                    if lemma:
                        cleanLemma = symbolPattern.sub('', lemma)
                        if cleanLemma:
                            lemmas.append(cleanLemma)
        
        uniqueLemmas = list(OrderedDict.fromkeys(lemmas))
        return uniqueLemmas
    
    def TypeTokenRatio(self, lemmaList, wordsList):
        TTR_result = len(lemmaList) / len(wordsList)
        return round(TTR_result, 2)
    
    def directSpeech(self, analysisList, sentencesTotal):
        directSpeechCount = 0
        directSpeechExample = []

        for teikums_key, teikums_value in analysisList.items():
            sentences = teikums_value.get('sentences', [])
            for sentence in sentences:
                tokens = sentence.get('tokens', [])
                for i in range(len(tokens) - 1):
                    if tokens[i].get('lemma') == ':' and tokens[i + 1].get('lemma') == '"':
                        directSpeechExample.append({
                            'teksts': teikums_value.get('text'),
                        })
                        directSpeechCount += 1

        return round(directSpeechCount / len(sentencesTotal), 2), json.dumps(directSpeechExample, indent=2, ensure_ascii=False)
        
    def simpleSentence(self, sentenceType, sentencesTotal):
        data = json.loads(sentenceType)
        simpleSentenceCount = sum(1 for teikums_list in data.values() for teikums_dict in teikums_list if teikums_dict.get('uzbuve') == 'Vienkāršs')
        return round(simpleSentenceCount / len(sentencesTotal), 2)

    def rarityClassification(self, lemmas, threshold=6000):
        tree = ET.parse('LVK2022.xml')
        root = tree.getroot()
        word_frequencies = {}

        for item in root.findall('./wordlist/item'):
            token = item.find('str').text
            frequency = int(item.find('freq').text)

            if token in lemmas:
                word_frequencies[token] = frequency

        classifications = {}
        for word in lemmas:
            if word in word_frequencies:
                frequency = word_frequencies[word]
                if frequency < threshold:
                    classifications[word] = 'RETS'
                else:
                    classifications[word] = 'nav rets'
            else:
                classifications[word] = 'RETS'

        return classifications
    
    def rarityRatio(self, rareList):
        rareCount = sum(1 for value in rareList.values() if value == 'RETS')
        foundLemmaCount = sum(1 for value in rareList.values())
        ratio = rareCount / foundLemmaCount
        return round(ratio, 2)

    def LVNLPAnalysis(self, sentencesSplit):
        api_url = 'https://nlp.ailab.lv/api/nlp'
        results = {}
        
        steps = None or ['tokenizer', 'morpho', 'parser', 'ner']

        for i, sentence in enumerate(sentencesSplit, start=1):
            payload = {'data': {'text': sentence}, 'steps': steps}
            r = requests.post(api_url, json=payload)
            
            if r.status_code == 200:
                data = r.json().get('data')
                results[f"Teikums #{i}"] = data
            else:
                results[f"Teikums #{i}"] = f"Error: {r.status_code}"
        
        return json.dumps(results, indent=2, ensure_ascii=False)

    def evaluate(self):
        asl = self.ASL()

        words = self.tokenize()

        syllables = self.syllableize(words)

        asw = self.ASW(syllables)

        longWords = self.longWords()

        lvLasamiba = self.lvLasamibasMeginajums(longWords)
        lvLasamiba_result = self.lvLasamibas_grade(lvLasamiba)

        flesch_reading_ease_result = self.flesch_reading_ease(asl, asw)
        flesch_reading_grade_result = self.flesch_reading_grade(flesch_reading_ease_result)

        complex_words = self.complex_words(syllables)
        cws_result = self.CWS(words, complex_words)

        gunning_fog_index_result = self.gunning_fog_index(asl, cws_result)
        gunning_fog_index_grade = self.gunning_fog_grade(gunning_fog_index_result)

        sentences = self.tokenizeSent()

        lvnlpanalysisData = self.LVNLPAnalysis(sentences)
        parsedAnalysisData = json.loads(lvnlpanalysisData)

        NERRatio, NERExample = self.NERRatio(parsedAnalysisData, words)
    
        sentenceType = self.sentence_type(parsedAnalysisData)

        avgCommas = self.average_comma_count()
        
        directSpeechProportion, directSpeechExamples = self.directSpeech(parsedAnalysisData, sentences)

        simpleSentenceProportion = self.simpleSentence(sentenceType, sentences)

        lemmas = self.getLemma(parsedAnalysisData)

        TypeTokenRatio = self.TypeTokenRatio(lemmas, words)

        rarityList = self.rarityClassification(lemmas)
        rarityProportion = self.rarityRatio(rarityList)

        response = {
            "teksts" : self.text,
            "vid_teikuma_gar": asl,
            "vid_varda_gar": longWords,
            "vid_zilbju_gar": asw,
            "zilbju_saraksts": self.syllableize(words),
            "sarezgitie_vardi": complex_words,
            "vid_komatu_skaits_teik": avgCommas,
            "lv_meginajuma_koef": lvLasamiba,
            "lv_meginajuma_klase": lvLasamiba_result,
            "flesch_koef": flesch_reading_ease_result,
            "flesch_klase": flesch_reading_grade_result,
            "gunning_fog_index": gunning_fog_index_result,
            "gunning_fog_klase": gunning_fog_index_grade,
            "tiesas_runas": directSpeechExamples,
            "tiesas_runas_svars": directSpeechProportion,
            "teikumu_uzbuve": sentenceType,
            "vienkarso_teikumu_svars": simpleSentenceProportion,
            "visi_vardi": words,
            "unikalie_vardi": lemmas,
            "unikalo_vardu_svars": TypeTokenRatio,
            "reto_vardu_svars": rarityProportion,
            "reto_vardu_saraksts": rarityList,
            "nosauktas_entitates": NERExample,
            "nosauktas_entitates_svars": NERRatio
        }

        return response

@app.route("/favicon.ico")
def favicon():
    return url_for('static', filename='data:,')

@app.route('/statistics', methods=['GET'])
def submit():
    text = request.args.get('text')
    if text is None:
        return "Datnes saturs nesatur tekstu."

    evaluator = ComplexityEval(text)
    response = evaluator.evaluate()
    response = jsonify(response)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/untrained_predict', methods=['GET'])
def predict():

    text = request.args.get('text')
    if text is None:
        return "Datnes saturs nesatur tekstu."
    
    prediction = best_model.predict([text])

    prediction_serializable = [x.item() if isinstance(x, np.int64) else x for x in prediction]
    
    return jsonify({'prediction': prediction_serializable[0]})


if __name__ == "__main__":
    app.run(port=8080)
    

