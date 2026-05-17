<#import "template.ftl" as layout>

<@layout.registrationLayout displayInfo=false; section>
  <#if section = "form">
    <h2>Terms and Conditions</h2>

    <p>Welcome to our platform. By using this service, you agree to the following terms:</p>

    <ul>
      <li>You will not misuse the platform.</li>
      <li>Your data will be processed according to our privacy policy.</li>
      <li>Unauthorized access and abuse are strictly prohibited.</li>
    </ul>

    <form id="kc-terms-form" action="${url.loginAction}" method="post">
      <div>
        <input type="checkbox" id="accept" name="accept" required>
        <label for="accept">I have read and accept the Terms and Conditions</label>
      </div>

      <div style="margin-top: 1rem;">
        <button type="submit" class="btn btn-primary">Accept</button>
      </div>
    </form>
  </#if>
</@layout.registrationLayout>
