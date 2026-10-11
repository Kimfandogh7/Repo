import type { OpenSlideConfig } from '@open-slide/core';

const openSlideConfig: OpenSlideConfig = {
  // لازم است برای اینکه پیش‌نمایش از طریق هاستِ e2b باز شود؛
  // وگرنه Vite با 403 "Host is not allowed" جواب می‌دهد.
  allowedHosts: true,
};

export default openSlideConfig;
