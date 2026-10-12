document.addEventListener('DOMContentLoaded', () => {
  const uploadArea = document.getElementById('uploadArea');
  const fileInput = document.getElementById('fileInput');
  const selectFileBtn = document.getElementById('selectFileBtn');
  const statusBox = document.getElementById('statusBox');
  const statusText = document.getElementById('statusText');

  const openFilePicker = () => {
    if (fileInput) fileInput.click();
  };

  if (selectFileBtn) selectFileBtn.addEventListener('click', openFilePicker);
  if (uploadArea) uploadArea.addEventListener('click', openFilePicker);

  if (fileInput) {
    fileInput.addEventListener('change', async (event) => {
      const file = event.target.files[0];
      if (!file) return;
      await uploadFile(file);
    });
  }

  const uploadFile = async (file) => {
    const formData = new FormData();
    formData.append('file', file);

    statusBox.classList.remove('hidden');
    statusText.textContent = 'Processing file...';

    try {
      const response = await fetch('/convert', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.error || 'Could not convert file.');
      }

      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = file.name.replace(/\.[^/.]+$/, '') + '.pdf';
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
      statusText.textContent = 'Download ready.';
    } catch (error) {
      statusText.textContent = error.message || 'Conversion failed.';
    }
  };
});
