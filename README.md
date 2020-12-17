# klippa_assessment

Een applicatie waarmee Klippa's OCR API aangeroepen kan worden om bonnen en facturen mee te verwerken. Je stuurt een afbeelding of PDF in en krijgt een JSON response van de API terug. Gerealiseerd in Python. Ik heb geprobeerd dit in Go te doen maar daar kwam ik niet direct uit.

## De applicatie kan het volgende
 1. De API key als optie mee geven
 1. De template als optie mee geven
 1. PDF text extraction fast of full als optie mee geven
 1. Een bestand mee kunnen geven die hij verwerkt via de OCR API (PDF of afbeelding)
 1. Het resultaat van de verwerking mooi weergeven
 1. De optie mee geven om de json output op te slaan bij het bestand als {bestandsnaam}.json
 1. Het kunnen meegeven van een map ipv 1 bestand en de hele map als batch kunnen verwerken
 1. Een map monitoren, dus als er een nieuw bestand in de map komt deze automatisch verwerken (passief en proactief)
    1. proactief zorgt ervoor dat nieuwe bestanden ook verwerkt worden.
 1. Bovenstaande dingen vinden concurrent plaats, dus als je een hele map verwerkt verwerkt je gelijktijdig meerdere files

## Hoe te runnen?

Runtime environment maken en de volgende parameters meegeven: 

--key **Je OCR API key** --path **Het pad waar je bestanden staan**  --monitor proactive --text_extraction full --template financial --store_output yes


[De documentatie voor de OCR API is hier te vinden](https://custom-ocr.klippa.com/docs)
