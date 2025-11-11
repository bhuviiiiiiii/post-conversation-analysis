from textblob import TextBlob
from datetime import datetime
import nltk
from nltk.tokenize import sent_tokenize
from .models import Conversation, ConversationAnalysis

class ConversationAnalyzer:
    def __init__(self):
        # Download required NLTK data
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt')
    
    def analyze_conversation(self, conversation):
        messages = conversation.messages.all().order_by('timestamp')
        if not messages:
            return None

        # Calculate various metrics
        clarity_score = self._calculate_clarity_score(messages)
        relevance_score = self._calculate_relevance_score(messages)
        sentiment_result = self._analyze_sentiment(messages)
        empathy_score = self._calculate_empathy_score(messages)
        accuracy_score = self._calculate_accuracy_score(messages)
        completeness_score = self._calculate_completeness_score(messages)
        response_time = self._calculate_response_time(messages)
        resolution_score = self._calculate_resolution_score(messages)
        escalation_needed = self._check_escalation_needed(messages)
        fallback_count = self._count_fallbacks(messages)
        
        # Calculate overall score
        overall_score = self._calculate_overall_score([
            clarity_score, relevance_score, empathy_score,
            accuracy_score, completeness_score, resolution_score
        ])
        
        # Create or update analysis
        analysis, _ = ConversationAnalysis.objects.update_or_create(
            conversation=conversation,
            defaults={
                'clarity_score': clarity_score,
                'relevance_score': relevance_score,
                'sentiment': sentiment_result,
                'empathy_score': empathy_score,
                'accuracy_score': accuracy_score,
                'completeness_score': completeness_score,
                'response_time_avg': response_time,
                'resolution_score': resolution_score,
                'escalation_needed': escalation_needed,
                'fallback_count': fallback_count,
                'overall_score': overall_score
            }
        )
        
        return analysis

    def _calculate_clarity_score(self, messages):
        # Analyze sentence structure and readability for AI messages
        clarity_scores = []
        for message in messages:
            if message.sender == 'ai':
                text = message.text
                sentences = sent_tokenize(text)
                
                # Simple readability score based on sentence length and complexity
                avg_sentence_length = sum(len(s.split()) for s in sentences) / len(sentences)
                normalized_length = min(1.0, 20 / avg_sentence_length) # Optimal length ~20 words
                
                clarity_scores.append(normalized_length)
        
        return sum(clarity_scores) / len(clarity_scores) if clarity_scores else 0.0

    def _calculate_relevance_score(self, messages):
        # Check if AI responses address user queries
        relevance_scores = []
        for i in range(len(messages) - 1):
            if messages[i].sender == 'user' and messages[i+1].sender == 'ai':
                user_text = TextBlob(messages[i].text.lower())
                ai_text = TextBlob(messages[i+1].text.lower())
                
                # Calculate similarity between user question and AI response
                similarity = self._calculate_text_similarity(user_text, ai_text)
                relevance_scores.append(similarity)
        
        return sum(relevance_scores) / len(relevance_scores) if relevance_scores else 0.0

    def _analyze_sentiment(self, messages):
        # Analyze user message sentiment
        user_sentiments = []
        for message in messages:
            if message.sender == 'user':
                blob = TextBlob(message.text)
                user_sentiments.append(blob.sentiment.polarity)
        
        avg_sentiment = sum(user_sentiments) / len(user_sentiments) if user_sentiments else 0
        
        if avg_sentiment > 0.2:
            return 'positive'
        elif avg_sentiment < -0.2:
            return 'negative'
        return 'neutral'

    def _calculate_empathy_score(self, messages):
        empathy_indicators = [
            'understand', 'sorry', 'apologize', 'help',
            'appreciate', 'thank', 'please', 'would you'
        ]
        
        empathy_scores = []
        for message in messages:
            if message.sender == 'ai':
                text = message.text.lower()
                score = sum(1 for indicator in empathy_indicators if indicator in text)
                normalized_score = min(1.0, score / 3)  # Normalize with max of 3 indicators
                empathy_scores.append(normalized_score)
        
        return sum(empathy_scores) / len(empathy_scores) if empathy_scores else 0.0

    def _calculate_accuracy_score(self, messages):
        # Simplified accuracy score based on consistency of AI responses
        # In a real implementation, this would need domain-specific validation
        return 0.85  # Placeholder

    def _calculate_completeness_score(self, messages):
        completeness_scores = []
        for message in messages:
            if message.sender == 'ai':
                # Check if response has multiple sentences and sufficient length
                sentences = sent_tokenize(message.text)
                word_count = len(message.text.split())
                
                has_multiple_sentences = len(sentences) > 1
                has_sufficient_length = word_count >= 20
                has_greeting = any(greeting in message.text.lower() 
                                 for greeting in ['hello', 'hi', 'thanks', 'thank you'])
                
                score = (has_multiple_sentences + has_sufficient_length + has_greeting) / 3
                completeness_scores.append(score)
        
        return sum(completeness_scores) / len(completeness_scores) if completeness_scores else 0.0

    def _calculate_response_time(self, messages):
        response_times = []
        for i in range(len(messages) - 1):
            if messages[i].sender == 'user' and messages[i+1].sender == 'ai':
                time_diff = (messages[i+1].timestamp - messages[i].timestamp).total_seconds()
                response_times.append(time_diff)
        
        return sum(response_times) / len(response_times) if response_times else 0.0

    def _calculate_resolution_score(self, messages):
        # Check for resolution indicators in the last few messages
        last_messages = messages.order_by('-timestamp')[:3]
        resolution_indicators = [
            'solved', 'resolved', 'fixed', 'completed', 'done',
            'helped', 'thank you', 'thanks', 'great', 'perfect'
        ]
        
        for message in last_messages:
            if message.sender == 'user':
                text = message.text.lower()
                if any(indicator in text for indicator in resolution_indicators):
                    return 1.0
        return 0.0

    def _check_escalation_needed(self, messages):
        # Check for frustration indicators or complex issues
        frustration_indicators = [
            'not working', 'still not', 'wrong', 'incorrect',
            'frustrated', 'angry', 'upset', 'escalate', 'supervisor',
            'manager', 'not helping', 'useless'
        ]
        
        for message in messages:
            if message.sender == 'user':
                text = message.text.lower()
                if any(indicator in text for indicator in frustration_indicators):
                    return True
        return False

    def _count_fallbacks(self, messages):
        # Count instances where AI uses fallback responses
        fallback_indicators = [
            "i don't know", "i'm not sure", "i cannot", "i can't",
            "unable to", "don't understand", "cannot help"
        ]
        
        count = 0
        for message in messages:
            if message.sender == 'ai':
                text = message.text.lower()
                if any(indicator in text for indicator in fallback_indicators):
                    count += 1
        return count

    def _calculate_overall_score(self, scores):
        # Calculate weighted average of all scores
        return sum(scores) / len(scores) if scores else 0.0

    def _calculate_text_similarity(self, text1, text2):
        # Simple similarity based on common words
        words1 = set(text1.words)
        words2 = set(text2.words)
        
        if not words1 or not words2:
            return 0.0
            
        common_words = words1.intersection(words2)
        return len(common_words) / max(len(words1), len(words2))