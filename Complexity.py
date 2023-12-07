import requests
import json
import re
import nltk
import spacy
from nltk.tokenize import sent_tokenize, word_tokenize
requests.packages.urllib3.disable_warnings()


class ComplexityEval:
    def __init__(self, text):
        self.text = text

    def clean(self):
        cleansed_words = re.sub(r'[^\w\s]', '', self.text)
        return cleansed_words

    def tokenize(self):
        cleansed_words = self.clean()
        tokens = word_tokenize(cleansed_words)
        return tokens

    def tokenizeSent(self):
        cleansed_sent = sent_tokenize(self.text)
        return cleansed_sent

    # ASL jeb Average Sentence Length noskaidro, cik vidēji garš teikums ir.
    # ASL metrika = Kopējais vārdu skaits starp visiem teikumiem / Kopējais teikumu skaits
    def ASL(self):
        # Definē, kas ir teikums (Teksta vienība atdalīta ar beigu simbolu)
        sentences = re.split('[.!?]', self.text)
        # Noņem empty string sentences (tikai, ja eksistē teikums)
        sentences = [sentence for sentence in sentences if sentence.strip()]
        # Izveido sarakstu ar visiem vārdiem. Viens saraksta elements = viens vārds.
        # Ar len() metodi noskaidro saraksta garumu.
        words = self.tokenize()
        word_count = len(words)
        # Ar len() metodi noskaidro cik teikumi ir tekstā.
        sentences_count = len(sentences)
        # Aprēķina vidējo garumu teikumam.
        asl = word_count / sentences_count
        return asl

    def replace_hyphens(self, data):
        return data.replace('<span class="hyphen">•</span>', '-')

    def syllableize(self, wordList):
        session = requests.Session()
        syllablesList = []
        response = session.get('https://www.ushuaia.pl/hyphen', verify=False)
        cookie = session.cookies.get_dict()
        if response.status_code == 200:
            if response:
                print(f'Pieslēgts cookie auth: ', cookie['hyphen'])
            else:
                print(f"Cookie auth error: {response.status_code}")
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
        print(hyphen_counts)
        asw = sum(hyphen_counts) / len(hyphen_counts) if len(hyphen_counts) > 0 else 0
        return asw

    def flesch_reading_ease(self, asl, asw):
        metric_result = 206.835 - (1.015 * asl) - (84.6 * asw)
        return metric_result
    
    def flesch_reading_grade(self, flesch_reading_ease):
        grade_meaning = ""
        if flesch_reading_ease >= 90:
            grade_meaning = "Very easy to read. Vecuma līmenis: 9 gadi un zemāk"
        elif flesch_reading_ease >= 80:
            grade_meaning = "Easy to read. Vecuma līmenis: 9 gadi un zemāk"
        elif flesch_reading_ease >= 70:
            grade_meaning = "Fairly easy to read. Vecuma līmenis: 10 gadi"
        elif flesch_reading_ease >= 60:
            grade_meaning = "Plain English. Vecuma līmenis: 11 - 13 gadi"
        elif flesch_reading_ease >= 50:
            grade_meaning = "Fairly difficult to read. Vecuma līmenis: 13-15 gadi"
        elif flesch_reading_ease >= 30:
            grade_meaning = "Difficult to read. Līmenis: koledžas"
        elif flesch_reading_ease >= 10:
            grade_meaning = "Very difficult to read. Līmenis: koledžas absolvents"
        elif flesch_reading_ease >= 0:
            grade_meaning = "Extremely difficult to read. Līmenis: profesionāla"
        else:
            grade_meaning = "Nesekmīgi"

        return grade_meaning
    
    def complex_words(self, syllables):
        words_to_remove = []
        for word in syllables:
            hyphen_count = word.count('-')
            hyphen_count = hyphen_count + 1
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
        return metric_result

    def gunning_fog_grade(self, gunning_fog_grade):
        grade_meaning = ""
        if gunning_fog_grade >= 20:
            grade_meaning = "Post-graduate +"
        elif gunning_fog_grade >= 17:
            grade_meaning = "Post-graduate"
        elif gunning_fog_grade >= 16:
            grade_meaning = "College senior"
        elif gunning_fog_grade >= 13:
            grade_meaning = "College junior"
        elif gunning_fog_grade >= 11:
            grade_meaning = "High school senior"
        elif gunning_fog_grade >= 10:
            grade_meaning = "High school sophomore"
        elif gunning_fog_grade >= 9:
            grade_meaning = "High school freshman"
        elif gunning_fog_grade < 9:
            grade_meaning = "Middle school and below"
        else:
            grade_meaning = "Nesekmīgi"

        return grade_meaning
    
    def sentence_structure(self, sentence):
        url = f"http://api.tezaurs.lv:8182/morphotagger/{sentence}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.text
            lines = data.split('\n')
            modified_lines = ['\t\t'.join(line.split()[:2] + line.split()[3:]) for line in lines if line.strip()]
            modified_data = '\n'.join(modified_lines)
            return modified_data
        else:
            return f"Error: {response.status_code}"

    def sentence_structure_define(self, posTags):
        has_conjunctor = False
        has_subordinator = False
        for i in range(len(posTags) - 1):
            if posTags[i] == 'zc' and posTags[i + 1] == 'cc' or posTags[i] == 'zc' and i < len(posTags) - 1 and posTags[i + 1] != 'cs':
                has_conjunctor = True
            if posTags[i] == 'zc' and posTags[i + 1] == 'cs' or posTags[i] == 'zc' and 'r0' in posTags[i + 1]:
                has_subordinator = True

        if has_subordinator and has_conjunctor:
            return "Jaukts salikts"
        elif has_conjunctor:
            return "Salikts sakārtots"
        elif has_subordinator:
            return "Salikts pakārtots"
        else:
            return "Vienkāršs"
    
    def getWordAnalysis(self, words):
        analysisList = []
        for word in words:
            url = f"http://api.tezaurs.lv:8182/analyze/{word}"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                if data:
                    analysisList.append(data)
                else:
                    print("Nav atrasti dati vārdam:", word)
            else:
                return f"Error: {response.status_code}"

        fields = []
        for items in analysisList:
            for item in items:
                field_dict = {
                    "Vārds": item.get("Vārds"),
                    "Mija": item.get("Mija"),
                }
                if "Izteiksme" in item:
                    field_dict["Izteiksme"] = item.get("Izteiksme")
                if "Pakāpe" in item:
                    field_dict["Pakāpe"] = item.get("Pakāpe")
                if "Kārta" in item:
                    field_dict["Kārta"] = item.get("Kārta")
                fields.append(field_dict)
        return fields

    def LVNLPAnalysis(self):
        text = self.text
        api_url='https://nlp.ailab.lv/api/nlp'
        steps = None or ['tokenizer', 'morpho', 'parser', 'ner']
        r = requests.post(api_url, json={'data': {'text': text}, 'steps': steps})
        data = r.json()
        data = data['data']
        data = json.dumps(data, indent=2, ensure_ascii=False)
        return data

    def evaluate(self):

        print("----------------TEKSTA SAREŽĢĪTĪBA------------------------\n\n")

        print("----------------Lasāmības atribūtika------------------------\n")

        asl_result = self.ASL()
        
        words = self.tokenize()

        syllables = self.syllableize(words)
        print("Zilbju saraksts:\n", syllables, '\n')

        asw = self.ASW(syllables)

        flesch_reading_ease_result = self.flesch_reading_ease(asl_result, asw)
        print(f"Fleša lasīšanas viegluma aprēķins: ", flesch_reading_ease_result)

        flesch_reading_grade_result = self.flesch_reading_grade(flesch_reading_ease_result)
        print(f"Fleša – Kinkeida lasīšanas viegluma klase: ", flesch_reading_grade_result, '\n')

        complex_words = self.complex_words(syllables)
        # print(f"Sarežģītie vārdi: ", complex_words)
        cws_result = self.CWS(words, complex_words)
        gunning_fog_index_result = self.gunning_fog_index(asl_result, cws_result)

        print(f"Gunning fog indekss: ",gunning_fog_index_result)

        gunning_fog_index_grade = self.gunning_fog_grade(gunning_fog_index_result)

        print(f"Gunning fog klase: ", gunning_fog_index_grade)

        print("\n\n----------------Teikuma uzbūve------------------------\n")

        print(f"Vidējais zilbju daudzums vārdā (ASW): {asw}")
        print(f"Vidējais teikuma garums (ASL): {asl_result}\n")

        sentences = self.tokenizeSent()

        sentences_tags = []
        sentence_types_count = {'Jaukts salikts': 0, 'Salikts sakārtots': 0, 'Salikts pakārtots': 0, 'Vienkāršs': 0}
        for i, sentence in enumerate(sentences, start=1):
            structure = self.sentence_structure(sentence)
            print("#",i,f"Teikuma: '{sentence.strip()}' morfoloģiskās birkas:\n{structure}\n")
            rindas = structure.split('\n')
            birkas = [rinda.split('\t\t')[1] for rinda in rindas] 
            # print("#",i,f"Teikuma birkas:", birkas, '\n')   
            sentence_type = self.sentence_structure_define(birkas)
            if sentence_type in sentence_types_count:
                sentence_types_count[sentence_type] += 1
            print("#",i,f"Teikuma tips: ", sentence_type, '\n\n')
        
        print("Teksta kopējās teikuma uzbūves daļas: \n",sentence_types_count)

        print("\n\n----------------Vārdu analīze------------------------\n")

        analysedWords = self.getWordAnalysis(words)
        formattedAnalysedWords = json.dumps(analysedWords, indent=4, ensure_ascii=False)
        analysedWords = [dict(t) for t in set(tuple(d.items()) for d in analysedWords if isinstance(d, dict))]
        formattedAnalysedWords = json.dumps(analysedWords, indent=4, ensure_ascii=False)
        print("Vārdu analīze:", formattedAnalysedWords)
        print(sentences)

        lvnlpanalysisData = self.LVNLPAnalysis()
        print("LV NLP analīze: ", lvnlpanalysisData)

def main():
    text = '''Viņa lasa, jo es negribu. Atskan zvans no kaimiņa. Studenti mācās universitātē, bet skolēni - skolā. Kad saule riet, zvaigznes parādās debesīs. Lai gan viņš ir prasmīgs vīrs, viņam nebija laika izdarīt savu darbu tāpēc, ka kārtība prasa laiku.'''
    evaluator = ComplexityEval(text)
    evaluator.evaluate()

if __name__ == "__main__":
    main()