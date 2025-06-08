document.addEventListener('DOMContentLoaded', function() {
  const facultyForm = document.getElementById('facultyForm');
  const resultsContainer = document.getElementById('results');
  const facultyResults = document.getElementById('facultyResults');

  facultyForm.addEventListener('submit', function(e) {
    e.preventDefault();

    // Заглушка: всегда рекомендуем ФИТ
    resultsContainer.classList.remove('hidden');
    facultyResults.innerHTML = `
      <div class="faculty-card">
        <h3 class="faculty-card__title">ФИТ — Факультет инновационных технологий</h3>
        <p class="faculty-card__description">
          🎉 Поздравляем! На основе ваших интересов и выбранных предметов мы рекомендуем вам <b>ФИТ</b>.<br>
          Здесь вы сможете изучать программирование, искусственный интеллект, современные IT-технологии и создавать инновационные проекты.<br>
          <br>
          <span style="color:#2088e9;">ФИТ — это путь к востребованным профессиям будущего!</span>
        </p>
        <button class="btn btn-primary btn-lg" onclick="alert('Подача заявки пока недоступна в демо-версии')">
          Подать заявку
        </button>
      </div>
    `;

    // Прокрутить к результату
    resultsContainer.scrollIntoView({behavior: "smooth"});
  });
});