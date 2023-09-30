from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Choice, Question, Vote


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())

    def get(self, request, *args, **kwargs):
        question = self.get_object()

        # Check if voting is allowed for this question
        if not question.can_vote():
            messages.error(request, "Voting is not allowed for this question.")
            return redirect('polls:index')

        # Check if the user has already voted for this question
        previous_vote = None
        if request.user.is_authenticated:
            previous_vote = Vote.objects.filter(user=request.user, choice__question=question).first()

        return render(request, self.template_name, {
            'question': question,
            'previous_vote': previous_vote,  # Pass the user's previous vote to the template
        })


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


@login_required
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    if not question.can_vote():
        messages.error(request,
                       f'Voting not currently accepted for "{question.question_text}".')
        return redirect('polls:index')

    this_user = request.user

    try:
        # find a vote for this user and this question
        vote = Vote.get_vote(user=this_user, choice__question=question)
        # update this vote
        vote.choice = selected_choice
    except Vote.DoesNotExist:
        # no matching vote - create a new vote
        vote = Vote(user=this_user, choice=selected_choice)

    vote.save()
    # Display a confirmation on the results page.
    messages.success(request, "Vote success!")

    # Always return an HttpResponseRedirect after successfully dealing
    # with POST data. This prevents data from being posted twice if a
    # user hits the Back button.
    return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
