from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
# from therapy.models import DASS21Statements as DASS21 


statements = {
    "statements": [
        {
            "statement": "I found it hard to wind down",
            "label": "Stress"
        },
        {
            "statement": "I was aware of dryness of my mouth",
            "label": "Anxiety"
        },
        {
            "statement": "I couldn\u2019t seem to experience any positive feeling at all",
            "label": "Depression"
        },
        {
            "statement": "I experienced breathing difficulty (e.g. excessively rapid breathing, breathlessness in the absence of physical exertion)",
            "label": "Anxiety"
        },
        {
            "statement": "I found it difficult to work up the initiative to do things",
            "label": "Depression"
        },
        {
            "statement": "I tended to over-react to situations",
            "label": "Stress"
        },
        {
            "statement": "I experienced trembling (e.g. in the hands)",
            "label": "Anxiety"
        },
        {
            "statement": "I felt that I was using a lot of nervous energy",
            "label": "Stress"
        },
        {
            "statement": "I was worried about situations in which I might panic and make a fool of myself",
            "label": "Anxiety"
        },
        {
            "statement": "I felt that I had nothing to look forward to",
            "label": "Depression"
        },
        {
            "statement": "I found myself getting agitated",
            "label": "Stress"
        },
        {
            "statement": "I found it difficult to relax",
            "label": "Stress"
        },
        {
            "statement": "I felt down-hearted and blue",
            "label": "Depression"
        },
        {
            "statement": "I was intolerant of anything that kept me from getting on with what I was doing",
            "label": "Stress"
        },
        {
            "statement": "I felt I was close to panic",
            "label": "Anxiety"
        },
        {
            "statement": "I was unable to become enthusiastic about anything",
            "label": "Depression"
        },
        {
            "statement": "I felt I wasn\u2019t worth much as a person",
            "label": "Depression"
        },
        {
            "statement": "I felt that I was rather touchy",
            "label": "Stress"
        },
        {
            "statement": "I was aware of the action of my heart in the absence of physical exertion (e.g. sense of heart rate increase, heart missing a beat)",
            "label": "Anxiety"
        },
        {
            "statement": "I felt scared without any good reason",
            "label": "Anxiety"
        },
        {
            "statement": "I felt that life was meaningless",
            "label": "Depression"
        }
    ]
}


answers = {
    "answers": [
        {
            "scale": 0,
            "short_answer": "NEVER",
            "detailed_answer": "Did not apply to me at all"
        },
        {
            "scale": 1,
            "short_answer": "SOMETIMES",
            "detailed_answer": "Applied to me to some degree, or some of the time"
        },
        {
            "scale": 2,
            "short_answer": "OFTEN",
            "detailed_answer": "Applied to me to a considerable degree, or a good part of time"
        },
        {
            "scale": 3,
            "short_answer": "ALMOST ALWAYS",
            "detailed_answer": "Applied to me very much, or most of the time"
        }
    ]
}


@csrf_exempt
def serve_statements(request): return JsonResponse(statements)

@csrf_exempt
def serve_answers(request): return JsonResponse(answers)



    
