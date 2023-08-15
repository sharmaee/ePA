<template>
  <PriorHeader />
  <div class="missing-requirements-wrapper">
    <h1 :class="{ hide: screenWidth < 835 }">Request Call for Critera</h1>
    <p>Our Agents are On Stand-By to Find what you need to submit. Current expected Turnaround: x</p>
    <div class="shadow-ellipse shadow-ellipse-right"></div>
    <div class="request-missing-requirements-form-wrapper">
      <div class="missing-requirements-form">
        <h2>Get the exact preparation steps your patient needs.</h2>
        <hr />
        <form action="">
          <div class="row-with-two-input">
            <div class="patient-name">
              <label for="patient-name">Patient Name</label>
              <input id="patient-name" type="text" placeholder="eg. John" />
            </div>
            <div class="patient-last-name">
              <label for="patient-last-name">Patient Last Name</label>
              <input id="patient-last-name" type="text" placeholder="eg. Snow" />
            </div>
          </div>

          <div class="row-with-two-input">
            <div class="date-of-birth">
              <label for="date-of-birth">Date Of Birth</label>
              <input id="date-of-birth" type="text" placeholder="eg. MM/DD/YYYY" />
            </div>
            <div class="patient-member-id">
              <label for="patient-member-id">Patient Member ID</label>
              <input id="patient-member-id" type="text" placeholder="eg. H3485045" />
            </div>
          </div>

          <div class="row-with-one-input">
            <label for="patient-phone-number">Patient Phone Number</label>
            <input id="patient-phone-number" type="text" placeholder="eg. +1-XXX-XXX-XXXX" />
          </div>

          <div class="row-with-one-input">
            <label for="patient-plan-type">Patient Plan Type</label>
            <input id="patient-plan-type" type="text" placeholder="eg. Medicare, Commercial, Medicaid " />
          </div>

          <div class="row-with-one-input">
            <label for="patient-address">Patient Address</label>
            <input id="patient-address" type="text" placeholder="eg. 541 Addison Ave, Palo " />
          </div>

          <div class="row-with-two-input">
            <div class="referring-doctor">
              <label for="referring-doctor">Referring Doctor</label>
              <input id="referring-doctor" type="text" placeholder="eg. Aetna" />
            </div>
            <div class="your-email">
              <label for="your-email">Your Email</label>
              <input id="your-email" type="text" placeholder="example@findsunrise.com" />
            </div>
          </div>
          <span class="agreement">
            By clicking the button below, I authorize service providers acting on behalf of Quantification by Design
            Inc. dba Lamar Health (“Lamar Health”) to obtain, use, share, disclose, and store the patient's personal and
            medical information to provide access support (“Support”). I understand that such Support may require
            contact with: applicable health insurer(s); and any pharmacy involved in my (or the patient's) treatment. I
            understand that I do not need to sign this form in order to obtain treatment, insurance, or insurance
            benefits; I am required to sign it only if I wish to receive optional Lamar Health support. I understand I
            can revoke my authorization at any time by emailing my revocation to security@lamarhealth.com.
          </span>
          <button>Email me info</button>
        </form>
      </div>
    </div>
    <div class="shadow-ellipse shadow-ellipse-left"></div>
  </div>
  <PriorFooter />
</template>

<script setup>
import { ref } from "vue";
import PriorHeader from "@/components/PriorHeader";
import PriorFooter from "@/components/PriorFooter";

const screenWidth = ref(null);

function displayWindowSize() {
  screenWidth.value = document.documentElement.clientWidth;
}

window.addEventListener("resize", displayWindowSize);

displayWindowSize();
</script>

<style lang="sass" scoped>
@import "../styles/pages/_request-missing-requirements"
</style>
