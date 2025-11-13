import { CommonModule } from '@angular/common';
import { Component, inject } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { FloatingBackgroundComponent } from '@/app/components/ui/floating-background.component';
import { UbButtonDirective } from '@/app/components/ui/button';
import { OptimizedImageComponent } from '@/app/components/ui/optimized-image.component';
import { environment } from '@/environments/environment';
import { ToastService } from '@/app/components/ui/toast.service';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    FloatingBackgroundComponent,
    UbButtonDirective,
    OptimizedImageComponent,
  ],
  templateUrl: './login.component.html',
  styleUrl: './login.component.css',
})
export class LoginComponent {
  loginObj: any = {
    username: '',
    password: '',
  };
  private readonly demoCredentials = environment.demoLogin;
  private readonly toast = inject(ToastService);

  readonly featureHighlights = [
    {
      title: 'Smart Dashboards',
      description:
        'Monitor people, projects & assignments in a single view with real-time insight.',
    },
    {
      title: 'Lightning Onboarding',
      description:
        'Invite new teammates, provision access & share documentation in a few clicks.',
    },
    {
      title: 'Predictive Analytics',
      description:
        'Anticipate resourcing needs with automated forecasting and talent signals.',
    },
  ];

  router = inject(Router);

  onLogin() {
    if (
      this.loginObj.username === this.demoCredentials.username &&
      this.loginObj.password === this.demoCredentials.password
    ) {
      this.router.navigateByUrl('dashboard');
      this.toast.success({
        title: 'Welcome back!',
        description: 'You have been signed in successfully.',
      });
    } else {
      this.toast.error({
        title: 'Invalid credentials',
        description: 'Please double check your username and password.',
      });
    }
  }
}
